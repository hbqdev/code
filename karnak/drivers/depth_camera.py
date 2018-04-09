# Copyright 2013 Google Inc. All Rights Reserved.

"""Helper functions for depth cameras."""
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
import numpy as np
import png
from primesense import openni2
import scipy.ndimage
from model import camera_pb2
from model import depth_image_mesher_pb2 as dim
from model import swivel_scan_manifest_pb2 as ssm
from google.protobuf import text_format

# Executable name constants (all paths relative to the base directory, nominally
# /scan/katamari/scanning-ops/karnak/static)
CALIBRATION_TOOL_EXECUTABLE = '../depth_camera/calibration-tool'
DEPTH_IMAGE_MESHER_EXECUTABLE = '../depth_camera/depth_image_mesher_tool'

# Output filename constants
CALIBRATION_REQUEST_FILENAME = 'scan.tgz'
MESH_REQUEST_FILENAME = 'mesh_request.bin'
MANIFEST_FILENAME = 'manifest.proto'
PROCESSING_DIR = 'depth_camera'
MULTI_CAMERA_CALIBRATION_FILENAME = 'MultiCameraCalibration.bin'


class DepthCameraController(object):
  """Manages depth camera scanning and processing."""

  def __init__(self, is_calibration, is_swivel, scanner2d, depth_cameras,
               capture_dir, calibration_filename):
    self._is_calibration = is_calibration
    self._is_swivel = is_swivel
    self._scanner = scanner2d
    self._depth_cameras = depth_cameras
    self._capture_dir = capture_dir
    self._processing_dir = os.path.join(capture_dir, PROCESSING_DIR)
    self._calibration_filename = calibration_filename
    self._depth_threads = []

  def InitializeCameras(self, delay=5):
    """Initializes the camera drivers and allow auto-exposure to settle."""
    for camera, _ in self._depth_cameras:
      camera.StartDriver()
    self._scanner.exclude_pattern = 'depth_camera'
    # Sleep to let the depth camera auto-exposure settle
    time.sleep(delay)

  def ShutdownCameras(self):
    """Unloads the camera drivers.  Also stops any captures."""
    self.StopCapture()
    for camera, _ in self._depth_cameras:
      camera.StopDriver()

  def StartCapture(self, degree, empty_mode, filename_function, verbose):
    """Starts capturing data from all connected depth cameras.

    Call after InitializeCameras but before ShutdownCameras.
    Args:
      degree: Rotation of the turntable in degrees.
      empty_mode: Is this an empty scan?
      filename_function: Function taking a camera, rotation, and empty flag
        and returning a filename for this capture.
      verbose: Use verbose logging.
    """
    self._depth_threads = []
    for camera, seq in self._depth_cameras:
      self._depth_threads.append(
          camera.StartStreaming(self._capture_dir,
                                filename_function(camera, degree, empty_mode),
                                seq,
                                verbose=verbose,
                                is_calibration=self._is_calibration))

  def StopCapture(self):
    """Stops capturing data from all connected depth cameras.

    Call after InitializeCameras and StartStreaming but before ShutdownCameras.
    """
    for camera, _ in self._depth_cameras:
      camera.StopStreaming()

  def ProcessScan(self, manifest):
    """Processes the depth imagery collected from the scan."""
    if self._is_calibration:
      # Write manifest first so that calibration-tool can read it
      if not os.path.exists(self._capture_dir):
        os.makedirs(self._capture_dir)
      with open(os.path.join(self._capture_dir, MANIFEST_FILENAME), 'w') as f:
        f.write(manifest.SerializeToString())
      calibration_dir = os.path.join(
          self._scanner.config.base_directory,
          self._scanner.config.station.calibration_directory)
      Calibrate(self._scanner.config.base_directory, self._capture_dir,
                self._calibration_filename, calibration_dir)
    elif self._is_swivel:
      if not os.path.exists(self._processing_dir):
        os.makedirs(self._processing_dir)
      CopyScanToProcessingDir(manifest, self._processing_dir)
      print 'Copied/linked scan to processing directory'
      calibration_path = os.path.join(self._capture_dir,
                                      self._calibration_filename)
      LoadCalibration(manifest, calibration_path, self._processing_dir)
      for _, seq in self._depth_cameras:
        CreateMeshShells(self._scanner.config.base_directory,
                         dim.DepthImageMesherOptions(), seq,
                         self._processing_dir)
      CopyMeshesToCaptureDir(manifest, self._capture_dir, self._processing_dir)


def CopyScanToProcessingDir(manifest, processing_dir):
  """Writes the manifest and links its files to the processing directory."""
  manifest_path = os.path.join(processing_dir, MANIFEST_FILENAME)
  manifest_txt_path = os.path.join(processing_dir, MANIFEST_FILENAME + '.txt')

  with open(manifest_path, 'w') as f:
    f.write(manifest.SerializeToString())
  with open(manifest_txt_path, 'w') as f:
    f.write(text_format.MessageToString(manifest))

  for seq in manifest.image_sequences:
    if seq.HasField('empty_filename'):
      os.symlink(os.path.join('../', seq.empty_filename),
                 os.path.join(processing_dir, seq.empty_filename))
    for f in seq.filenames:
      os.symlink(os.path.join('../', f), os.path.join(processing_dir, f))


def LoadCalibration(scan_object, calibration_path, processing_dir):
  """Loads calibration from an on-disk proto and adds it to the ScanObject.

  Args:
    scan_object: The scan object.
    calibration_path: Path to the MultiCameraCalibration proto.
    processing_dir: The processing directory.

  Raises:
    LookupError: If there is a mismatch between MultiCameraCalibration and the
      cameras in the ScanObject.
  """
  # Read the calibration file and fill out the manifest's calibration fields.
  with open(calibration_path, 'r') as f:
    contents = f.read()
    mcc = camera_pb2.MultiCameraCalibration.FromString(contents)

  # Create a link to the calibration proto within the processing directory.
  os.symlink(os.path.join('../', os.path.basename(calibration_path)),
             os.path.join(processing_dir, os.path.basename(calibration_path)))

  for camera in mcc.cameras:
    calibration_id = camera.information.camera_number
    for seq in scan_object.image_sequences:
      seq_id = seq.camera_information.camera_number
      if calibration_id == seq_id:
        seq.intrinsic.CopyFrom(camera.intrinsic)
        seq.extrinsic.CopyFrom(camera.extrinsic)
        break
    else:
      raise LookupError


def Calibrate(base_dir, calibration_dir, calibration_filename,
              calibration_output_dir):
  """Computes intrinsics and extrinsics.

  Args:
    base_dir: Base karnak directory.
    calibration_dir: Directory with the calibration scan images.
    calibration_filename: Desired filename for the calibration scan proto
      (will be put in the calibration_dir).
    calibration_output_dir: Where to put the final output.
  """
  # Write calibration scan to a tar file
  # TODO(jarussell): Let calibration-tool read directly from a directory.
  tarball_path = os.path.join(tempfile.gettempdir(),
                              CALIBRATION_REQUEST_FILENAME)
  with tarfile.open(name=tarball_path, mode='w:gz') as tarball:
    tarball.add(calibration_dir, '.')

  calibration_path = os.path.join(calibration_output_dir,
                                  calibration_filename)
  executable_path = os.path.join(base_dir, CALIBRATION_TOOL_EXECUTABLE)
  call_list = [executable_path,
               '--logtostderr',
               '--scan_filename=' + tarball_path,
               '--geometry2d=true',
               '--output_directory=' + calibration_dir,
               '--save_segmented_images=true',
               '--save_calibration_images=true',
               '--use_gradient_cut_threshold=false']
  print 'executable_path: ' + executable_path
  print 'calibration_path: ' + calibration_path
  Subprocess(call_list)

  # Copy result to the desired location (if necessary)
  calibration_tool_output_path = os.path.join(calibration_dir,
                                              MULTI_CAMERA_CALIBRATION_FILENAME)
  try:
    shutil.copyfile(calibration_tool_output_path, calibration_path)
  except shutil.Error:
    print 'Could not copy calibration file (already in the right place?)'


def CreateMeshShells(base_dir, options, scan_image_sequence, processing_dir):
  """Generates PLY meshes from a series of depth images.

  Args:
    base_dir: Base karnak directory.
    options: DepthImageMesherOptions proto.
    scan_image_sequence: ScanImageSequence proto for the scan.
    processing_dir: Write output to this directory.
  """
  # Generate mesh paths by swapping the extension
  mesh_filenames = []
  for filename in scan_image_sequence.filenames:
    mesh_filenames.append(GetCanonicalMeshFilename(filename))

  request_path = os.path.join(processing_dir, MESH_REQUEST_FILENAME)
  WriteMeshRequest(request_path, options, scan_image_sequence,
                   mesh_filenames, processing_dir, processing_dir)

  executable_path = os.path.join(base_dir, DEPTH_IMAGE_MESHER_EXECUTABLE)
  call_list = [executable_path, '--input=' + request_path, '--logtostderr']
  print 'executable_path: ' + executable_path
  print 'request_path: ' + request_path
  Subprocess(call_list)


def CopyMeshesToCaptureDir(manifest, capture_dir, processing_dir):
  """Copies mesh shells to the capture directory.

  Args:
    manifest: The ScanObject.
    capture_dir: Capture directory in which to put meshes.
    processing_dir: Directory containing the meshes.

  Raises:
    shutil.Error: If there is a problem copying meshes.
  """
  filenames = []
  for image_sequence in manifest.image_sequences:
    if image_sequence.camera_position == ssm.ScanImageSequence.DEPTH:
      for image_filename in image_sequence.filenames:
        filenames.append(GetCanonicalMeshFilename(image_filename))

  for f in filenames:
    try:
      shutil.copyfile(os.path.join(processing_dir, f),
                      os.path.join(capture_dir, f))
    except shutil.Error:
      raise


def WriteMeshRequest(request_path, options, scan_image_sequence,
                     mesh_filenames, capture_dir, output_dir):
  """Writes a DepthImageMesherRequest to files (both binary and text format).

  The text format proto will append ".txt" to the binary filename.

  Args:
    request_path: Where to write the request protos.
    options: DepthImageMesherOptions message (if None, use default values).
    scan_image_sequence: ScanImageSequence message for the depth camera.
    mesh_filenames: List of filenames for writing the output meshes.
    capture_dir: Directory containing the capture imagery.
    output_dir: Directory to put the meshes.

    The number of mesh_filenames must equal the number of filenames in the
    scan_image_sequence.
  """
  mesh_proto = dim.DepthImageMesherRequest()
  if options is not None:
    mesh_proto.options.CopyFrom(options)
  mesh_proto.capture_directory = capture_dir
  mesh_proto.output_directory = output_dir
  mesh_proto.depth_capture_sequence.CopyFrom(scan_image_sequence)
  for path in mesh_filenames:
    mesh_proto.mesh_filenames.append(path)
  with open(request_path + '.txt', 'w') as f:
    f.write(text_format.MessageToString(mesh_proto))
  with open(request_path, 'w') as f:
    f.write(mesh_proto.SerializeToString())


def Subprocess(call_list):
  """Runs a subprocess, piping output to stdout.

  Args:
    call_list: Call list for subprocess.

  Raises:
    subprocess.CalledProcessError: If the subprocess does not return normally.
  """
  try:
    print 'Starting depth camera subprocess; this may take a while...'
    print subprocess.check_output(call_list, stderr=subprocess.STDOUT)
    print '...subprocess finished normally'
  except subprocess.CalledProcessError as retval:
    print 'Process exited with code %d' % retval.returncode
    raise


def GetCanonicalMeshFilename(depth_image_filename):
  """Gets the canonical filename for a mesh given a depth image input."""
  (root, _) = os.path.splitext(depth_image_filename)
  return root + '.ply'


def WriteToPNG(filename, data_array):
  """Writes a single frame to a PNG file.

  If single channel, writes a 1-channel, 16-bit Grayscale PNG.
  If three channel, writes a 3-channel, 8-bit RGB PNG.

  Args:
    filename: Path to output file
    data_array: The numpy array of data to write
  """
  # Open file for writing.
  try:
    pngfile = open(filename, 'w')
  except IOError:
    raise IOError('Could not open output file %s' % filename)

  if len(data_array.shape) == 2:
    # Make the grayscale PNG writer
    writer = png.Writer(width=data_array.shape[1],
                        height=data_array.shape[0],
                        greyscale=True,
                        bitdepth=16,
                        compression=0)
    writer.write(pngfile, data_array)
  elif data_array.shape[2] == 3:
    # Make the RGB PNG writer
    writer = png.Writer(width=data_array.shape[1],
                        height=data_array.shape[0],
                        greyscale=False,
                        bitdepth=8,
                        compression=9)
    writer.write(pngfile,
                 np.reshape(data_array,
                            (-1, data_array.shape[1] * data_array.shape[2])))


def AverageDepthImages(images, max_std_dev=100):
  """Computes an average depth image from a list of captures.

  This is only useful if each capture is from the same pose. Pixels with a
  standard deviation greater than max_std_dev are set to 0.

  Args:
    images: List of numpy ndarray images.
    max_std_dev: Maximum tolerable standard deviation.

  Returns:
    mean_image: The mean image (in float64)
  """
  assert images
  as_array = np.asarray(images)
  std_dev = np.std(as_array, 0)
  mean = np.mean(as_array, 0)
  mean[std_dev > max_std_dev] = 0
  return mean


class DepthSensor(object):
  """Base class for structured light depth sensors.
  """

  def __init__(self, rotate_degrees):
    if rotate_degrees not in (0, 90, 180, 270):
      print 'rotate_degrees must be a multiple of 90'
      raise ValueError
    self._rotate_degrees = rotate_degrees

  def Start(self):
    raise NotImplementedError

  def Stop(self):
    raise NotImplementedError

  def Capture(self, is_calibration=False):
    raise NotImplementedError

  def WriteToFile(self, data, filename):
    if filename.endswith('.png'):
      WriteToPNG(filename, data)
    else:
      raise ValueError

  def Rotate(self, data):
    return np.rot90(data, self._rotate_degrees / 90)


class PrimesenseImpl(DepthSensor):
  """Class to implement the PrimeSense sensor via OpenNI2.
  """

  def __init__(self, guid=None, rotate_degrees=0):
    """Configures the PrimesenseCamera.

    Args:
      guid: the ID of the camera (if none, first device will be used)
      rotate_degrees: The roll of the camera
    """
    DepthSensor.__init__(self, rotate_degrees)
    self._guid = guid

  def Start(self):
    if not openni2.is_initialized():
      openni2.initialize()
    if self._guid is not None:
      self._dev = openni2.Device.open_file(self._guid)
    else:
      self._dev = openni2.Device.open_any()

    self._rgb = self._dev.create_color_stream()
    self._rgb.set_video_mode(openni2.VideoMode(
        pixelFormat=openni2.PIXEL_FORMAT_RGB888,
        resolutionX=1280,
        resolutionY=1024,
        fps=30))
    self._rgb.start()
    self._depth = self._dev.create_depth_stream()
    self._depth.set_video_mode(openni2.VideoMode(
        pixelFormat=openni2.PIXEL_FORMAT_DEPTH_100_UM,
        resolutionX=640,
        resolutionY=480,
        fps=30))
    self._depth.start()

    self._dev.set_image_registration_mode(
        openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)

  def Stop(self):
    openni2.unload()

  def __del__(self):
    self.Stop()

  def Capture(self, output_color=False):
    """Captures a single frame from a Primesense sensor.

    Args:
      output_color: True, output RGB stream rather than depth

    Returns:
      image as a numpy ndarray.
    """
    color_frame = self._rgb.read_frame()
    depth_frame = self._depth.read_frame()

    if output_color:
      self._max_value = 255
      frame = color_frame
    else:
      self._max_value = 65535
      frame = depth_frame

    if output_color:
      data = frame.get_buffer_as_uint8()
      data = np.ctypeslib.as_array(data)
      data = np.reshape(data, (1024, 1280, 3), 'A')
    else:
      data = frame.get_buffer_as_uint16()
      data = np.ctypeslib.as_array(data)
      data = np.reshape(data, (480, 640), 'A')
      # Reformat to 1280 x 1024 so we can re-use high res calibration
      # The scheme used here has been verified to be pixel-perfect on the RD1.09
      # Carmine sensor.
      data = scipy.ndimage.zoom(data, 2, order=0)
      data = np.vstack((np.zeros((32, 1280)), data, np.zeros((32, 1280))))

    # Primesense cameras are always flipped horizontally.
    data = np.fliplr(data)

    return self.Rotate(data)
