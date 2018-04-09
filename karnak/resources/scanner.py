# Copyright 2013 Google Inc. All Rights Reserved.

"""Scan station model and controller."""
from multiprocessing import Process
import os
import shutil
import sys
import threading
import time
import yaml
try:
  # Optional module.
  from drivers import depth_camera
  from model import depth_image_mesher_pb2 as dim
except ImportError:
  depth_camera = dim = None
  print >> sys.stderr, "Cannot import depth_camera."

from model import swivel_scan_manifest_pb2
from resources import camera
from resources import crosshair
from resources import errors
from resources import katamari
from resources import lighting
from resources import shoe_light
from resources import stepper


# TODO(arshan): Change the config driven aspect to include more of a script for
#  scan behaviours, swivel,calibration, daily, etc.
FAKE_SCAN_SEGMENTS = 72
# TODO(kwc): pull into config.
CALIBRATION_SEGMENTS = 36
DAILY_SEGMENTS = 18

CALIBRATION_FILENAME = "MultiCameraCalibration.bin"

# Convenience constants.
FRONT = swivel_scan_manifest_pb2.ScanImageSequence.FRONT
TOP = swivel_scan_manifest_pb2.ScanImageSequence.TOP
ORTHO = swivel_scan_manifest_pb2.ScanImageSequence.ORTHO
BOTTOM = swivel_scan_manifest_pb2.ScanImageSequence.BOTTOM
DEPTH = swivel_scan_manifest_pb2.ScanImageSequence.DEPTH

DEFAULT_KATAMARI_ID = "K0000000000"
MANIFEST_FILENAME = "manifest.proto"
META_NAME_FILENAME = "fullname.meta"
UPLOAD_LOCK_FILENAME = "uploaded.lock"

CAPTURE_TYPE_DAILY = "daily"
CAPTURE_TYPE_CALIBRATION = "calibration"
CAPTURE_TYPE_EMPTY = "empty"
CAPTURE_TYPE_SWIVEL = "swivel"
CAPTURE_TYPE_TEST = "test"

# Scanner statuses
# TODO(katydek): Investigate moving to a protocol buffer
STATUS_DOWN = "STATUS_DOWN"
STATUS_UP = "STATUS_UP"

# Scanner states
# TODO(katydek): Investigate moving to a protocol buffer
STATE_READY = "STATE_READY"
STATE_SCANNING = "STATE_SCANNING"
STATE_STARTUP = "STATE_STARTUP"
STATE_SHUTDOWN = "STATE_SHUTDOWN"
STATE_FAULT = "STATE_FAULT"


TABLE_MAP = {
    "WHITE_WOOD": swivel_scan_manifest_pb2.ScanImageSequence.WHITE_WOOD,
    "GLASS": swivel_scan_manifest_pb2.ScanImageSequence.GLASS,
    }


def Register(factory):
  factory.RegisterFromDict("Scanner2d", Scanner2d.FromDict)
  factory.RegisterFromDict("OrthoTable", OrthoTable.FromDict)


def FromDict(scanner, raw_config):
  scanner.table_type = TABLE_MAP[raw_config.get("table_type", "WHITE_WOOD")]
  scanner.starting_rotation_angle = raw_config.get("starting_rotation_angle", 0)
  katamari.FromDict(scanner, raw_config)


def GetScanDirectoryName(directory):
  if not directory:
    print "GetScanDirectoryName: directory not configured"
    return None
  path = os.path.join(directory, META_NAME_FILENAME)
  if os.path.exists(path):
    with open(path, "r") as f:
      return f.read()
  print "Attempt to find file/directory failed: %s" % path
  return ""


def GetProtoBuf(directory):
  """Deserialize the protobuf from the provided scan directory."""
  if not directory:
    print "GetProtoBuf: directory not configured"
    return None
  path = os.path.join(directory, MANIFEST_FILENAME)
  if os.path.exists(path):
    m = swivel_scan_manifest_pb2.ScanObject()
    with open(path, "r") as f:
      m.ParseFromString(f.read())
      return m
  print "Attempt to read protobuf failed, no file named : %s" % path
  return None


def CreateManifest(ss_config, katamari_id, operator_id=None):
  """Creates a new ScanObject manifest proto.

  Args:
    ss_config: ScannerConfig instance.
    katamari_id: The object's katamari id
    operator_id: The current operator's id
  Returns:
    Initialized ScanObject manifest.
  """
  m = swivel_scan_manifest_pb2.ScanObject()
  m.katamari_id = str(katamari_id)
  m.scan_station.id = str(ss_config.station.name)
  if ss_config.station.model is not None:
    m.scan_station.model_id = str(ss_config.station.model)
  m.scan_station.raw_config = yaml.dump(ss_config.raw_config)

  # Populate the calibration and daily names.
  m.color_calibration_scan_name = GetScanDirectoryName(
      ss_config.station.calibration_directory)
  m.daily_calibration_scan_name = GetScanDirectoryName(
      ss_config.station.daily_directory)

  if operator_id:
    m.scan_station.operator_id = str(operator_id)
    print "operator: %s" % operator_id
  return m


def LoadManifest(dir_path, station_id, katamari_id):
  """Loads the manifest and validates against parameters.

  Args:
    dir_path: Location of the manifest file
    station_id: Expected station id.
    katamari_id: Expected katamari id.
  Returns:
    The manifest
  """
  m = swivel_scan_manifest_pb2.ScanObject()
  swivel_manifest_path = os.path.join(dir_path, MANIFEST_FILENAME)
  if not os.path.isfile(swivel_manifest_path):
    raise errors.InternalError(
        "No existing manifest in capture directory")
  with open(swivel_manifest_path, "r") as f:
    m.ParseFromString(f.read())
  if m.katamari_id != katamari_id:
    raise errors.InternalError(
        "Loaded manifest does not match expected Katamari ID")
  elif m.scan_station.id != station_id:
    raise errors.InternalError(
        "Loaded manifest does not match expected station ID")
  return m


def WriteManifest(manifest, capture_dir, filename=MANIFEST_FILENAME):
  if not os.path.exists(capture_dir):
    os.makedirs(capture_dir)
  swivel_manifest_path = os.path.join(capture_dir, filename)
  with open(swivel_manifest_path, "w") as f:
    f.write(manifest.SerializeToString())
  return swivel_manifest_path


def CombineManifests(src, dest):
  """Given 2 manifests, merge sections about the scan output into the dest."""
  # grab the sequences from the src and append to dest.
  if src is None:
    raise errors.InternalError(
        "Attempt to combine from a null manifest.")
  if dest is None:
    raise errors.InternalError(
        "Attempt to combine to a null manifest.")
  dest.image_sequences.append(src.image_sequences)


def DuplicateSingleCameraManifest(manifest):
  """Duplicate ScanImageSequence to second CameraPosition if needed.

  UX guidelines require a FRONT or ORTHO camera. This method allows a scan
  to present the same sequence of images as both a FRONT and ORTHO camera
  for scanner configurations where there is only a single physical camera.

  Args:
    manifest: ScanObject
  """

  camera_positions = [s.camera_position for s in manifest.image_sequences]

  if FRONT in camera_positions and ORTHO in camera_positions:
    print "FRONT and ORTHO camera positions already present"
    return

  if FRONT not in camera_positions and ORTHO not in camera_positions:
    print "Neither FRONT nor ORHTO camera positions available"
    return

  new_position = (ORTHO if FRONT in camera_positions else FRONT)
  old_position = (FRONT if FRONT in camera_positions else ORTHO)

  new_sequence = manifest.image_sequences.add()

  for sequence in manifest.image_sequences:
    if sequence.camera_position == old_position:
      new_sequence.CopyFrom(sequence)
      new_sequence.camera_position = new_position
      print "copied %s to %s in manifest" % (old_position, new_position)
      return

  raise errors.InternalError("Failed to modify manifest")


def InitSequence(cam, seq, scanner, angular_increment_degrees):
  """Initializes metadata about this camera in sequence.

  Init does not occur if sequence is None or the camera is a PREVIEW
  camera.

  Args:
    cam: Camera to use for sequence metadata.
    seq: Sequence proto.
    scanner: The scanner
    angular_increment_degrees: The angle between steps
  """
  seq.empty_filename = CaptureFilename(cam, 0, True)
  seq.table_type = scanner.table_type
  seq.starting_rotation_angle_degrees = scanner.starting_rotation_angle
  seq.angular_increment_degrees = angular_increment_degrees
  cam.FillCameraInfo(seq.camera_information)
  cam.InitSequence(seq)


def UploadProcess(scanner, capture_dir, capture_type, manifest,
                  swivel_manifest_path):
  """Callback that uploads the scan."""
  working_dir = os.path.dirname(capture_dir)

  # Kick off deferred processing
  print "Kicking off pre-upload deferred processing"
  scanner.PreUpload()
  print "Pre-upload processing complete"

  pack = scanner.config.packer

  print "Creating tarball"
  if capture_type == CAPTURE_TYPE_CALIBRATION:
    tarball_name = "%s.tar" % pack.GetCalibrationAssetId(manifest,
                                                         "calibration2d")
  elif capture_type == CAPTURE_TYPE_DAILY:
    tarball_name = "%s.tar" % pack.GetCalibrationAssetId(manifest,
                                                         "daily2d")
  else:
    tarball_name = None
  output_file = pack.Create(capture_dir, manifest, tarball_name=tarball_name,
                            working_dir=working_dir,
                            exclude=scanner.GetExcludePattern())
  print "Wrote tarball", output_file
  if scanner.config.storage:
    for backend in scanner.config.storage:
      print "uploading to %s" % backend
      backend.UploadFiles(manifest.katamari_id, [output_file,
                                                 swivel_manifest_path])
    print "upload complete"
  else:
    print "no storage configured, not uploading"


class Scanner(katamari.KatamariResource):
  """Marker class for Scanner resources."""

  def __init__(self):
    self.config = None
    self.scan_callback = None
    self.table_type = None
    self.status = {"status": STATUS_DOWN,
                   "status_start_time": int(time.time()),
                   "state_start_time": int(time.time()),
                   "scanner_state": STATE_READY}

  def Init(self, config):
    self.config = config

  def GetActions(self):
    return {"start": self.StartScan, "stop": self.StopScan,
            "upload": self.UploadScan,
            "preview": self.Preview,
            "empty": self.StartScanEmpty,
            "calibration": self.StartScanCalibration,
            "daily": self.StartScanDaily,
            "test shot": self.StartScanTest,
            "half rotate": self.DoHalfRotation,
            "full rotate": self.DoCompleteRotation,
            "status down": self.SetStatusDown,
            "status up": self.SetStatusUp,
            "status": self.GetStatus}

  def SetScanCallback(self, callback):
    """Sets the callback for the Scanner to call after each camera capture.

    Args:
      callback: Function(filename, metadata), where metadata is a dictionary of
          key/value strings.
    """
    self.scan_callback = callback

  def ConfigureCapture(self, katamari_id, capture_directory=None,
                       capture_type=CAPTURE_TYPE_SWIVEL,
                       operator_id=None):
    """Configures capture operation and prepares disk.

    Creates the capture directory and swivel manifest as needed.
    Scanners may be chained together, so this will use the parameters
    to determine whether or not a scan is continuing an existing session
    or starting a new one.

    Args:
      katamari_id: Katamari ID of object being captured.
      capture_directory: If set, this capture is a continuation of a previous
          capture and this was the capture directory used for that.
      capture_type: One of the CAPTURE_TYPE_* values.
      operator_id: ID of operator performing capture.

    Returns:
      capture_directory: The capture directory
      manifest: The manifest object

    Raises:
      errors.InternalError: If misconfigured.
    """
    station = self.config.station
    base_dir = self.config.base_directory
    rel_capture_dir = station.capture_directory
    rel_calibration_dir = station.calibration_directory
    rel_test_dir = station.test_directory
    if not any((base_dir, rel_capture_dir, rel_calibration_dir, rel_test_dir)):
      self.SetScannerState(STATE_FAULT, int(time.time()))
      raise errors.InternalError("missing capture dir parameters")
    if capture_type in [CAPTURE_TYPE_EMPTY, CAPTURE_TYPE_CALIBRATION]:
      # Empty/calibration shots go into separate, shared directory.
      manifest = CreateManifest(self.config, katamari_id, operator_id)
      capture_directory = os.path.join(base_dir, rel_calibration_dir)
    elif capture_type == CAPTURE_TYPE_TEST:
      # Test shots go into their own directory.
      manifest = CreateManifest(self.config, katamari_id, operator_id)
      capture_directory = os.path.join(base_dir, rel_test_dir)
    elif capture_type == CAPTURE_TYPE_DAILY:
      print "setting up for a daily calibration run"
      # daily calibrations go into their own directory.
      rel_calibration_dir = station.daily_directory
      manifest = CreateManifest(self.config, katamari_id, operator_id)
      capture_directory = os.path.join(base_dir, rel_calibration_dir)
    elif capture_directory is None:
      # We are not continuing a previous scan, so create new timestamped
      # directory for new scan.
      manifest = CreateManifest(self.config, katamari_id, operator_id)
      rel_dir = self.config.packer.GetSwivelAssetId(manifest)
      capture_directory = os.path.join(base_dir, rel_capture_dir, rel_dir)
      if not os.path.isdir(capture_directory):
        os.makedirs(capture_directory)
      with open("%s/%s" % (capture_directory, META_NAME_FILENAME), "w") as f:
        f.write(rel_dir)
        f.close()
    else:
      # We continuing a previous scan, so load the partial manifest.
      capture_directory = os.path.join(base_dir, capture_directory)
      # Currently, do not revalidate operator ID as this bit of data is not a
      # hard fail.
      manifest = LoadManifest(capture_directory,
                              station.name,
                              katamari_id)
    return capture_directory, manifest

  def PrepareScan(self, cameras, capture_directory, capture_type):
    """Prepares scan, including copying in empty shots.

    Args:
      cameras: List of cameras used in scan.
      capture_directory: Directory that cameras will capture files into.
      capture_type: One of the CAPTURE_TYPE_* values.
    Raises:
      errors.ConfigError: If configuration checks fail.
      errors.Error: If empty shots are missing.
    """
    station = self.config.station
    calibration_dir = os.path.join(self.config.base_directory,
                                   station.calibration_directory)
    test_dir = os.path.join(self.config.base_directory,
                            station.test_directory)
    if not calibration_dir:
      #TODO(katydek): do these also put the station 'down' automatically?
      self.SetScannerState(STATE_FAULT, int(time.time()))
      raise errors.ConfigError("Calibration dir not configured")
    if not test_dir:
      self.SetScannerState(STATE_FAULT, int(time.time()))
      raise errors.ConfigError("Test dir not configured")
    if not os.path.isdir(calibration_dir):
      os.makedirs(calibration_dir)
    if not os.path.isdir(test_dir):
      os.makedirs(test_dir)
    if not os.path.exists(capture_directory):
      os.makedirs(capture_directory)
    if capture_type == CAPTURE_TYPE_SWIVEL:
      for c in cameras:
        if not c.PrepareScan():
          self.SetScannerState(STATE_FAULT, int(time.time()))
          raise errors.Error("Camera not ready for scan")

        filename = CaptureFilename(c, 0, True)
        expected = os.path.join(calibration_dir, filename)

        # If there is a depth camera present, make sure calibration is present
        if c.position == DEPTH:
          cal_path = os.path.join(calibration_dir, CALIBRATION_FILENAME)
          if not os.path.isfile(cal_path):
            self.SetScannerState(STATE_FAULT, int(time.time()))
            raise errors.Error("Missing calibration proto %s" % cal_path)
          dest_file = os.path.join(capture_directory, CALIBRATION_FILENAME)
          if os.path.exists(dest_file):
            if not os.path.samefile(cal_path, dest_file):
              os.remove(dest_file)
          shutil.copyfile(cal_path, dest_file)
        if not os.path.isfile(expected):
          self.SetScannerState(STATE_FAULT, int(time.time()))
          raise errors.Error("Missing calibration/empty shots: %s" % expected)
        dest_file = os.path.join(capture_directory, filename)
        if os.path.exists(dest_file):
          if not os.path.samefile(expected, dest_file):
            os.remove(dest_file)
          else:
            return
        shutil.copyfile(expected, dest_file)

  def StartScan(self, katamari_id=DEFAULT_KATAMARI_ID, operator_id=None,
                capture_directory=None, capture_type=CAPTURE_TYPE_SWIVEL):
    """Starts the scanning of object on turntable.

    This will create both the raw scan data and the scan manifest.

    Args:
      katamari_id: Katamari ID of object being scanned.
      operator_id: Operator's ID
      capture_directory: Capture directory
      capture_type: The type of scan
    """
    raise NotImplementedError

  def StartScanEmpty(self, operator_id=None, capture_directory=None):
    self.StartScan(operator_id=operator_id, capture_directory=capture_directory,
                   capture_type=CAPTURE_TYPE_EMPTY)

  def StartScanTest(self, operator_id=None, capture_directory=None):
    self.StartScan(operator_id=operator_id, capture_directory=capture_directory,
                   capture_type=CAPTURE_TYPE_TEST)

  def StartScanCalibration(self, katamari_id=DEFAULT_KATAMARI_ID,
                           operator_id=None, capture_directory=None):
    self.StartScan(katamari_id=katamari_id, operator_id=operator_id,
                   capture_directory=capture_directory,
                   capture_type=CAPTURE_TYPE_CALIBRATION)

  def StartScanDaily(self, katamari_id=DEFAULT_KATAMARI_ID,
                     operator_id=None, capture_directory=None):
    self.StartScan(katamari_id=katamari_id, operator_id=operator_id,
                   capture_directory=capture_directory,
                   capture_type=CAPTURE_TYPE_DAILY)
    self.UploadScan(katamari_id=katamari_id)

  def Preview(self, katamari_id=DEFAULT_KATAMARI_ID, operator_id=None,
              capture_directory=None, capture_type=CAPTURE_TYPE_SWIVEL):
    raise NotImplementedError

  def UploadScan(self, katamari_id=DEFAULT_KATAMARI_ID):
    raise NotImplementedError

  def StopScan(self):
    raise NotImplementedError

  def DoCompleteRotation(self):
    raise NotImplementedError

  def DoHalfRotation(self):
    raise NotImplementedError

  def PreUpload(self):
    pass

  def GetExcludePattern(self):
    return None

  def SetStatusDown(self):
    self.UpdateStatus({"status": STATUS_DOWN, "status_start_time": int(time.time())})

  def SetStatusUp(self):
    self.UpdateStatus({"status": STATUS_UP, "status_start_time": int(time.time())})

  def SetScannerState(self, state, time):
    """ Sets the state for the scanner

    Args:
      state: A string representing the scanner state.
      time: An integer timestamp at which the state started.
    """
    self.UpdateStatus({"scanner_state": state, "state_start_time": time});


class OrthoTable(Scanner):
  """Ortho scanner (for bottom shot)."""

  def __init__(self):
    super(OrthoTable, self).__init__()
    self.camera = None
    self.manifest = None
    self._initialized = False
    self._resource_names = None
    self._twod_scanner = None
    self._lighting = None

  @staticmethod
  def FromDict(raw_config):
    scanner = OrthoTable()
    scanner._resource_names = raw_config["resources"]
    FromDict(scanner, raw_config)
    return scanner

  def Init(self, config):
    super(OrthoTable, self).Init(config)
    for resource_name in self._resource_names:
      resource = config.GetResource(resource_name)
      if resource is None:
        raise errors.ConfigError("[OrthoTable] No resource named [%s]. "
                                 "Resources are: %s" %
                                 (resource_name, config.GetResourceNames()))
      if isinstance(resource, Scanner2d):
        self._twod_scanner = resource
      if isinstance(resource, camera.Camera):
        self.camera = resource
      if isinstance(resource, lighting.LightingController):
        self._lighting = resource
    if not self.camera:
      raise errors.ConfigError("[OrthoTable] No camera resource.")
    if not self._twod_scanner:
      raise errors.ConfigError("[OrthoTable] No Scanner2d resource.")
    self._initialized = True

  def StopScan(self):
    # Ortho table scanner isn't really interruptable, nor does it take long.
    return dict(status="halted")

  def StartScan(self, katamari_id=DEFAULT_KATAMARI_ID, operator_id=None,
                capture_directory=None, capture_type=CAPTURE_TYPE_SWIVEL):
    """Scans object on turntable.

    This will create both the raw scan data and the scan manifest.

    Args:
      katamari_id: Katamari ID of object being scanned.
      operator_id: ID of operator running scan station.
      capture_directory: Capture directory, relative to the config base
          directory.
      capture_type: If set, one of ["swivel", "calibration", "empty"], aka
          CAPTURE_TYPE_[SWIVEL|CALIBRATION|EMPTY].

    Returns:
      Dict(capture_directory -> status)
    """

    if not self._initialized:
      raise errors.InternalError("[OrthoTable]: Not initialized")
    if self._twod_scanner is None:
      raise errors.InternalError("[OrthoTable]: No Registered TwoD Scanner")

    capture_directory, self.manifest = self.ConfigureCapture(
        katamari_id, capture_directory, capture_type, operator_id)
    manifest = self.manifest
    self.manifest.capture_time_start = time.time()
    seq = manifest.image_sequences.add()
    self.PrepareScan([self.camera], capture_directory, capture_type)
    threading.Thread(target=self.RunScan,
                     args=(manifest, seq,
                           capture_directory, capture_type)).start()
    base_dir = self.config.base_directory
    rel_capture_dir = os.path.relpath(capture_directory, base_dir)
    return dict(capture_directory=rel_capture_dir, status="scanning")

  def Preview(self, katamari_id=DEFAULT_KATAMARI_ID, operator_id=None,
              capture_directory=None, capture_type=CAPTURE_TYPE_SWIVEL):

    self._lighting.SwitchToBottomLighting()
    c = self.camera
    c.Preview("static", "preview_%d.jpg" % c.camera_number)
    capture_data = dict(capture_index=0, capture_segments=1,
                        camera_name=c.name.encode("utf-8"),
                        scanner_name=self.name.encode("utf-8"))
    self.scan_callback("static/preview_%d.jpg" % c.camera_number,
                       capture_data)

    self._lighting.AllOff()

  def RunScan(self, manifest, seq, capture_directory,
              capture_type=CAPTURE_TYPE_SWIVEL):
    cam = self.camera
    callback = self.scan_callback
    empty_mode = capture_type == CAPTURE_TYPE_EMPTY
    lights = self._lighting

    InitSequence(cam, seq, self, 360)

    # TODO(arshan): this 270 should not be hardcoded here ...
    filename = CaptureFilename(cam, 270, empty_mode)

    if lights:
      lights.SwitchToBottomLighting()

    path = cam.Capture(capture_directory, filename, sequence=seq,
                       singleshot=True)

    if lights:
      lights.AllOff()

    if callback is not None:
      capture_data = dict(capture_index=0, capture_segments=1,
                          camera_name=cam.name.encode("utf-8"),
                          scanner_name=self.name.encode("utf-8"))
      path = os.path.join(capture_directory, filename)
      callback(path, capture_data)

    manifest.capture_time_end = time.time()

    DuplicateSingleCameraManifest(manifest)

    WriteManifest(manifest, capture_directory)

  def UploadScan(self, katamari_id=DEFAULT_KATAMARI_ID):
    pass

  def PreUpload(self):
    pass

def CaptureFilename(cam, degrees, empty_mode):
  extension = "jpg"
  if cam.GetFormat() == swivel_scan_manifest_pb2.ScanImageSequence.DEPTH_PPM:
    extension = "pgm"
  elif cam.GetFormat() == swivel_scan_manifest_pb2.ScanImageSequence.PNG:
    extension = "png"
  if not empty_mode:
    return "%d-%03d.%s" % (cam.camera_number, degrees, extension)
  else:
    return "empty-%s-000.%s" % (cam.camera_number, extension)


class Scanner2d(Scanner):
  """2D swivel scanner."""

  def __init__(self):
    super(Scanner2d, self).__init__()

    self._initialized = False
    self._resource_names = None
    self._controller = None

    # Named, public properties for controller to access.
    self.resources = None
    self.turntable = None
    self.lighting = None
    self.scan_segments = None
    self.config = None
    self.crosshair = None
    self._shoe_lights = None

    self.pre_upload_calls = []
    self.exclude_pattern = None

    # Minimize scene transition by doing full spins in different
    # scenes.
    # TODO(arshan): move to the yaml
    self.multi_spin = False

  @staticmethod
  def FromDict(raw_config):
    scanner = Scanner2d()
    FromDict(scanner, raw_config)

    scanner.scan_segments = raw_config["scan_segments"]
    scanner._resource_names = raw_config["resources"]
    return scanner

  def Init(self, config):
    """Initializes the scanner from the loaded config.

    Scanner2d initialize is two-pass so that it can access
    all of the loaded config objects.

    Args:
      config: Loaded Config instances.
    """
    super(Scanner2d, self).Init(config)
    self.SetScannerState(STATE_STARTUP, int(time.time()))

    # Currently ignore the lighting.
    self.resources = []
    for resource_name in self._resource_names:
      resource = config.GetResource(resource_name)
      if resource is None:
        self.SetScannerState(STATE_FAULT, int(time.time()))
        raise errors.ConfigError("[Scanner2d] No resource named [%s]. "
                                 "Resources are: %s" %
                                 (resource_name, config.GetResourceNames()))
      self.resources.append(resource)
      if isinstance(resource, stepper.Stepper):
        self.turntable = resource
        # Initialize the scan segments
        self.turntable.SetSegments(self.scan_segments)
      if isinstance(resource, lighting.LightingController):
        self.lighting = resource
      if isinstance(resource, crosshair.Crosshair):
        self.crosshair = resource
      if isinstance(resource, shoe_light.ShoeLightController):
        self._shoe_lights = resource

    if self.turntable is None:
      self.SetScannerState(STATE_FAULT, int(time.time()))
      raise errors.ConfigError("No turntable in config")
    if not [x for x in self.resources if isinstance(x, camera.Camera)]:
      self.SetScannerState(STATE_FAULT, int(time.time()))
      raise errors.ConfigError("No cameras in config")
    self.SetScannerState(STATE_READY, int(time.time()))
    self._initialized = True

  def DoCompleteRotation(self):
    self.turntable.FullTurn()

  def DoHalfRotation(self):
    self.turntable.HalfTurn()

  def Preview(self, katamari_id=DEFAULT_KATAMARI_ID, operator_id=None,
              capture_directory=None, capture_type=CAPTURE_TYPE_SWIVEL):

    cameras = [c for c in self.resources
               if isinstance(c, camera.Camera) and c.position is TOP]

    # Make sure all lights are on, and we leave them on for more previews.
    self.lighting.AllOn()

    for c in cameras:
      c.Preview("static", "preview_%d.jpg" % c.camera_number)
      capture_data = dict(capture_index=0, capture_segments=1,
                          camera_name=c.name.encode("utf-8"),
                          scanner_name=self.name.encode("utf-8"))
      self.scan_callback("static/preview_%d.jpg" % c.camera_number,
                         capture_data)

    self.lighting.AllOff()

  def StartScan(self, katamari_id=DEFAULT_KATAMARI_ID, operator_id=None,
                capture_directory=None, capture_type=CAPTURE_TYPE_SWIVEL,
                controller=None):
    """Starts scanning operation.

    Args:
      katamari_id: The object's katamari ID
      operator_id: The operator's ID
      capture_directory: Capture directory, relative to the config base
          directory.
      capture_type: If set, one of ["swivel", "calibration", "empty"], aka
          CAPTURE_TYPE_[SWIVEL|CALIBRATION|EMPTY].
      controller: Override default controller (for testing).

    Returns:
      Dictionary with scan parameters and status
    """
    if not self._initialized:
      raise errors.InternalError("[Scanner2d]: Not initialized")

    print "going to configure for capture of type : %s" % capture_type
    capture_directory, manifest = self.ConfigureCapture(
        katamari_id, capture_directory, capture_type, operator_id)
    self._controller = (Scan2dController(self, manifest, capture_directory,
                                         capture_type=capture_type)
                        if controller is None else controller)
    cameras = self._controller.GetCaptureCameras()
    self.PrepareScan(cameras, capture_directory, capture_type)
    threading.Thread(target=self._controller).start()
    base_dir = self.config.base_directory
    if not base_dir:
      raise errors.InternalError("[Scanner2d]: missing capture dir parameters")
    rel_capture_dir = os.path.relpath(capture_directory, base_dir)
    station_id = manifest.scan_station.id

    tarball_name = (
        self.config.packer.GetOutputName(rel_capture_dir)
        if self.config.packer else "")
    return dict(capture_directory=rel_capture_dir, status="scanning",
                station_id=station_id, filename=tarball_name)

  def StopScan(self):
    if self._controller is not None:
      self._controller.Stop()
      self._controller = None
      status = self.GetStatus()
      if status["scanner_state"] == 'STATE_SCANNING':
        self.SetScannerState(STATE_READY, int(time.time()))
    return self.GetStatus()

  def UploadScan(self, katamari_id=DEFAULT_KATAMARI_ID):
    if self._controller is not None:
      self._controller.Upload()
      return dict(status="uploading")
    else:
      return dict(status="no current scan")

  def PreUpload(self):
    print "Performing %d pre-upload tasks" % len(self.pre_upload_calls)
    for f in self.pre_upload_calls:
      f()

  def GetExcludePattern(self):
    return self.exclude_pattern


class Scan2dController(object):
  """Controller for the 2D swivel scanner."""

  def __init__(self, scanner, manifest, capture_dir,
               capture_type=CAPTURE_TYPE_SWIVEL):
    self.scanner = scanner
    self.manifest = manifest
    self.capture_dir = capture_dir
    self.capture_type = capture_type
    self.swivel_manifest_path = "unknown"
    self._depth_camera_controller = None

    # If enabled automatically upload scan at end of capture.
    self.auto_upload = False
    self.upload_requested = False
    self.ready_for_upload = False
    self.upload_lock = threading.RLock()

  def __call__(self):
    self.Run()

  def GetCaptureCameras(self):
    positions = [TOP, ORTHO, FRONT, DEPTH]
    return [c for c in self.scanner.resources
            if isinstance(c, camera.Camera) and c.position in positions]

  def PrepareController(self):
    """Prepare camera resources and image sequences for easy iteration."""
    manifest = self.manifest
    manifest.capture_time_start = time.time()
    # del manifest.image_sequences[:]
    seqs = manifest.image_sequences
    cameras = self.GetCaptureCameras()
    front_cameras = [(c, seqs.add()) for c in cameras if c.position == FRONT]
    top_cameras = [(c, seqs.add()) for c in cameras if c.position == TOP]
    ortho_cameras = [(c, seqs.add()) for c in cameras if c.position == ORTHO]
    depth_cameras = [(c, seqs.add()) for c in cameras if c.position == DEPTH]

    for c, seq in front_cameras + top_cameras + ortho_cameras + depth_cameras:
      InitSequence(c, seq, self.scanner, self._GetAngularIncrement(c.position))

    return front_cameras, top_cameras, ortho_cameras, depth_cameras

  def CreateGenericIndex(self, capture_dir, title):
    """Create a generic index page."""
    index = open("%s/index.html" % capture_dir, "w")
    index.write("<head><title>%s</title>" % title)
    index.write("</head><html><img src='https://sites.google.com/a/google.com/google-objects/_/rsrc/1314754130885/google-objects/ux/objects_logo-250.png' /><br><b>%s</b><br>" % title)

    # TODO(arshan): Add index for depth camera.

    index.write("<table>")

    index.write("<tr>")
    # TODO(arshan): fill this cell with metadata info.
    index.write("<td></td>")
    index.write("<td><a href='empty-40-000.jpg'><img onerror='this.style.display = \"none\"' width=320px src='empty-40-000.jpg' /></a></td>")
    index.write("<td><a href='40-270.jpg'><img onerror='this.style.display = \"none\"' src='40-270.tn.jpg' /></a></td>")
    index.write("</tr>")

    index.write("<tr>")
    for i in range(10, 40, 10):
      index.write("<td><a href='empty-%d-000.jpg'><img onerror='this.style.display = \"none\"' width=320px src='empty-%d-000.jpg' /></a></td>" % (i, i))
    index.write("</tr>")

    for x in range(0, 360, 5):
      index.write("<tr>")
      for i in range(10, 40, 10):
        if i is 10:
          index.write("<td><a href='%d-%03d.jpg'><div style='-webkit-transform:rotate(180deg);'><img onerror='this.style.display = \"none\"' src='%d-%03d.tn.jpg' /></div></a>" % (i, x, i, x))
        else:
          index.write("<td><a href='%d-%03d.jpg'><img onerror='this.style.display = \"none\"' src='%d-%03d.tn.jpg' /></a>" % (i, x, i, x))
      index.write("</tr>")
    index.write("</table>")
    # TODO(arshan): use the .tmpl stuff to template this content
    index.close()

  def _GetScanSegments(self):
    if self.capture_type in (CAPTURE_TYPE_EMPTY, CAPTURE_TYPE_TEST):
      return 1
    elif self.capture_type == CAPTURE_TYPE_CALIBRATION:
      return CALIBRATION_SEGMENTS
    elif self.capture_type == CAPTURE_TYPE_DAILY:
      return DAILY_SEGMENTS
    else:
      return self.scanner.scan_segments

  def _GetAngularIncrement(self, camera_position):
    if (camera_position not in [FRONT, ORTHO, DEPTH] and
        self.capture_type == CAPTURE_TYPE_SWIVEL):
      return 90
    else:
      return 360 / self._GetScanSegments()

  def RunIter(self, verbose=False):
    """Runs controller as a continuation.

    This runner yields after every long step.  When the generator is complete,
    the run has completed.  RunIter() does not check the Stop() flag.  Use the
    blocking Run() call instead to use Stop() semantics.

    Args:
      verbose: Verbose logging

    Yields:
      After every long step
    """
    # Reset the uploader state so past Upload calls don't affect this scan.
    with self.upload_lock:
      self.upload_requested = False
      self.ready_for_upload = False

    # Determine what capture profile we are using.
    self.pre_upload_calls = []
    capture_type = self.capture_type
    empty_mode = (capture_type == CAPTURE_TYPE_EMPTY)
    test_mode = (capture_type == CAPTURE_TYPE_TEST)
    depth_calibration = (capture_type == CAPTURE_TYPE_DAILY)
    depth_swivel = (capture_type == CAPTURE_TYPE_SWIVEL)
    scan_segments = self._GetScanSegments()
    self.scanner.turntable.SetSegments(scan_segments)

    # Capture dir has already been computed for us, so not dependent on mode.
    capture_dir = self.capture_dir

    front_cameras, top_cameras, ortho_cameras, depth_cameras = self.PrepareController()

    manifest = self.manifest
    turntable = self.scanner.turntable
    scan_callback = self.scanner.scan_callback
    lighting = self.scanner.lighting
    crosshair = self.scanner.crosshair

    # If the lighting never changes, then fast track the scan.
    fast_mode = lighting.isMonotonous()
    if fast_mode:
      print "Putting this scan into fast mode."

    degree = 0

    # Crate an index.html to make viewing the capture easy.
    self.CreateGenericIndex(capture_dir, GetScanDirectoryName(capture_dir))

    if crosshair is not None:
      crosshair.off()
    if lighting:
      lighting.SwitchToFrontLighting()

    self.SetScannerState(STATE_SCANNING, int(time.time()))

    if depth_cameras:
      self._depth_camera_controller = depth_camera.DepthCameraController(
          depth_calibration, depth_swivel, self.scanner, depth_cameras,
          capture_dir, CALIBRATION_FILENAME)
      self._depth_camera_controller.InitializeCameras()

    for i in range(scan_segments):
      if verbose:
        print "doing capture .. %d" % degree
      capture_data = dict(capture_index=i, capture_segments=scan_segments,
                          scanner_name=self.scanner.name.encode("utf-8"))

      # Start capturing depth data
      if depth_cameras:
        self._depth_camera_controller.StartCapture(degree, empty_mode,
                                                   CaptureFilename, verbose)

      # Always capture on the front and ortho cameras.
      # We use threads for the capture so we can run captures in parallel and
      # gain linear speedup in capture time.
      capture_threads = []
      callback_data = []

      for camera, seq in front_cameras + ortho_cameras:
        filename = CaptureFilename(camera, degree, empty_mode)
        t = camera.StartCapture(capture_dir, filename, seq, verbose=verbose)
        capture_threads.append(t)
        capture_data["camera_name"] = camera.name.encode("utf-8")
        path = os.path.join(capture_dir, filename)
        callback_data.append((path, capture_data.copy()))
        yield

      # If we are in fast mode, take the top shot too.
      if fast_mode and (degree % 90 == 0 or
                        capture_type != CAPTURE_TYPE_SWIVEL):
        if capture_type == CAPTURE_TYPE_SWIVEL:
          capture_data["capture_index"] = degree // 90
          capture_data["capture_segments"] = 4
        for camera, seq in top_cameras:
          # Perform blocking capture as there is nothing to parallelize.
          filename = CaptureFilename(camera, degree, empty_mode)
          t = camera.StartCapture(capture_dir, filename, seq, verbose=verbose)
          capture_threads.append(t)
          capture_data["camera_name"] = camera.name.encode("utf-8")
          path = os.path.join(capture_dir, filename)
          callback_data.append((path, capture_data.copy()))
          yield

      # Wait for captures to complete.
      for t in capture_threads:
        t.join()

      # Sanity Check the capture.
      for camera, seq in front_cameras + ortho_cameras:
        filename = CaptureFilename(camera, degree, empty_mode)
        path = os.path.join(capture_dir, filename)
        if not os.path.exists(path):
          self.SetScannerState(STATE_FAULT, int(time.time()))
          raise errors.InternalError("Unable to capture %s" % path)
        # TODO(arshan): also check for black frame, unexpected size? ie. too
        #   small means bad frame

      # Inform callbacks.
      if scan_callback:
        for path, capture_data in callback_data:
          scan_callback(path, capture_data)
          yield

      if not self.scanner.multi_spin and not fast_mode:
        if degree % 90 == 0 or capture_type != CAPTURE_TYPE_SWIVEL:
          # Capture only at %90 degrees for the top.
          if lighting:
            lighting.SwitchToTopLighting()
            # self.scanner._shoe_lights.on()
          if capture_type == CAPTURE_TYPE_SWIVEL:
            capture_data["capture_index"] = degree // 90
            capture_data["capture_segments"] = 4
          for camera, seq in top_cameras:
            # Perform blocking capture as there is nothing to parallelize.
            filename = CaptureFilename(camera, degree, empty_mode)
            camera.Capture(capture_dir, filename, seq, verbose=verbose)
            if scan_callback:
              capture_data["camera_name"] = camera.name
              path = os.path.join(capture_dir, filename)
              scan_callback(path, capture_data)
            yield
          if lighting:
            lighting.SwitchToFrontLighting()
            # self.scanner._shoe_lights.off()

      # Stop this depth capture just before rotating the turntable.
      if depth_cameras:
        self._depth_camera_controller.StopCapture()

      # Don't do the final turntable spin, as it is unnecessary.  This also
      # makes sure the turntable doesn't do a complete rotation when segments
      # is 1.  This does mean that the turntable does not complete a full
      # rotation at the end.
      if i != scan_segments - 1:
        turntable.StepOneSegment()
      degree += 360 / scan_segments
      yield

    if self.scanner.multi_spin and not fast_mode:
      lighting.SwitchToTopLighting()
      for i in (0, 90, 180, 270):
        if capture_type == CAPTURE_TYPE_SWIVEL:
          capture_data["capture_index"] = i / 90
          capture_data["capture_segments"] = 4
        for camera, seq in top_cameras:
          # Perform blocking capture as there is nothing to parallelize.
          filename = CaptureFilename(camera, i, empty_mode)
          camera.Capture(capture_dir, filename, seq, verbose=verbose)
          if scan_callback:
            capture_data["camera_name"] = camera.name
            path = os.path.join(capture_dir, filename)
            scan_callback(path, capture_data)
          yield

        turntable.TurnDegrees(90)

    if lighting:
      lighting.AllOff()
    if crosshair is not None:
      crosshair.on()

    manifest.capture_time_end = time.time()
    print "capture complete"

    self.SetScannerState(STATE_READY, int(time.time()))

    if empty_mode or test_mode:
      return

    # Process depth camera
    if depth_cameras:
      self._depth_camera_controller.ProcessScan(manifest)

    DuplicateSingleCameraManifest(manifest)

    self.swivel_manifest_path = WriteManifest(manifest, capture_dir)
    print "Wrote manifest", self.swivel_manifest_path

    # Lock to set ready for upload and check for a requested upload atomically.
    with self.upload_lock:
      self.ready_for_upload = True

      if self.auto_upload or self.upload_requested:
        print "Auto/deferred upload engaged."
        self.Upload()

  def Upload(self):
    # Lock to check if ready to upload and request upload atomically.
    with self.upload_lock:
      if self.ready_for_upload:
        self.ready_for_upload = False
        self.upload_requested = False
        Process(target=UploadProcess,
                args=(self.scanner, self.capture_dir, self.capture_type,
                      self.manifest, self.swivel_manifest_path)).start()
        print "Launched upload process."
      else:
        self.upload_requested = True
        print "Upload requested but scan not finished; will upload when ready"

  def CleanUp(self):
    lighting = self.scanner.lighting
    crosshair = self.scanner.crosshair
    if lighting:
      lighting.AllOff()
    if crosshair is not None:
      crosshair.on()
    with self.upload_lock:
      self.ready_for_upload = False
      self.upload_requested = False

  def Run(self, verbose=False):
    self._stop = False
    self._is_running = True
    try:
      scan_iter = self.RunIter(verbose=verbose)
      try:
        while not self._stop:
          scan_iter.next()
      except StopIteration:
        pass
      # Clean up only required in the case where scanner was externally
      # stopped.
      # TODO(arshan):
      if self._stop:
        self.CleanUp()

    finally:
      self._is_running = False
      if self._depth_camera_controller:
        self._depth_camera_controller.ShutdownCameras()

  def Stop(self):
    """Stops controller if Run() was called."""
    self._stop = True
