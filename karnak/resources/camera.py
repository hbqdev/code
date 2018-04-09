# Copyright 2012 Google Inc. All Rights Reserved.

"""Abstractions for the onboard cameras."""
import ast
import os
import re
import sys
import threading
import time
from model import swivel_scan_manifest_pb2
from model import camera_information_pb2
from resources import errors
from resources import executors
from resources import katamari

try:
  import Image  # pylint: disable=g-import-not-at-top
  import ImageDraw  # pylint: disable=g-import-not-at-top
except ImportError:
  Image = ImageDraw = None
  print >> sys.stderr, 'PIL is not installed, cannot use FakeCamera'

try:
  # Optional module.
  from drivers import depth_camera # pylint: disable=g-import-not-at-top
except ImportError:
  depth_camera = None
  print >> sys.stderr, "Cannot import depth_camera."

NUM_DEPTH_IMAGES_TO_AVERAGE = 5
PREVIEW = -1
# No inventory id.
NOID = 'NOID'
CANON_REBEL_T2I = 'Canon T2i'
CANON_REBEL_T4I = 'Canon T4i'
CANON_EOS_5DM2 = 'Canon 5DM2'
CANON_EOS_5DM3 = 'Canon 5DM3'

POSITION_MAP = {
    'FRONT': swivel_scan_manifest_pb2.ScanImageSequence.FRONT,
    'TOP': swivel_scan_manifest_pb2.ScanImageSequence.TOP,
    'ORTHO': swivel_scan_manifest_pb2.ScanImageSequence.ORTHO,
    'BOTTOM': swivel_scan_manifest_pb2.ScanImageSequence.BOTTOM,
    'DEPTH': swivel_scan_manifest_pb2.ScanImageSequence.DEPTH,
    'PREVIEW': PREVIEW,
    }


def Register(factory):
  factory.RegisterFromDict('WebCamera', WebCamera.FromDict)
  factory.RegisterFromDict('CanonCamera', CanonCamera.FromDict)
  factory.RegisterFromDict('ArtProjectCamera', ArtProjectCamera.FromDict)
  factory.RegisterFromDict('FakeCamera', FakeCamera.FromDict)
  factory.RegisterFromDict('PrimesenseCamera', PrimesenseCamera.FromDict)


def FromDict(cam, raw_config):
  """Fills common camera fields from config dictionary.

  Args:
    cam: Camera instance.
    raw_config: Config dictionary for camera.
  """
  cam.inverted = raw_config.get('inverted', False)
  cam.camera_number = raw_config['camera_number']
  position_str = raw_config['position']
  cam.position = POSITION_MAP[position_str]
  cam.inventory_id = raw_config.get('inventory_id', NOID)
  katamari.FromDict(cam, raw_config)


class Camera(katamari.KatamariResource):
  """Abstract base class for cameras."""

  def __init__(self,
               position=swivel_scan_manifest_pb2.ScanImageSequence.FRONT,
               angle_degrees=None,
               camera_number=None):
    super(Camera, self).__init__()
    self.position = position
    self.angle_degrees = angle_degrees
    self.camera_number = camera_number
    self.inventory_id = None
    self.inverted = False
    self.streaming_thread = None

  def Init(self, config):
    """Two-phase resource init API."""
    pass

  def GetActions(self):
    return {'capture': self.Capture, 'preview': self.Preview}

  def StartStreaming(self,
                     capture_dir,
                     filename,
                     sequence,
                     verbose=False,
                     is_calibration=False):
    """Spawn a thread that calls Stream on this camera.
    Args:
      capture_dir: Filesystem directory to capture into.
      filename: File to store the stream
      sequence: ImageSequence proto.
      verbose: If True, print to screen.
      is_calibration: If True, this is a calibration sequence
    """
    cap_kwargs = {'capture_dir': capture_dir,
                  'filename': filename,
                  'sequence': sequence,
                  'verbose': verbose,
                  'is_calibration': is_calibration}
    self.stop_streaming = False
    self.streaming_thread = threading.Thread(target=self.Stream,
                                             kwargs=cap_kwargs)
    self.streaming_thread.start()

  def Stream(self,
             capture_dir,
             filename,
             sequence,
             verbose=False,
             is_calibration=False):
    """Method called in its own thread when StartStreaming is called.

    Implementations should monitor for the self.stop_streaming flag to be set.
    Implementations may also want to implement a mutex to prevent Capture while
    streaming.
    Args:
      capture_dir: Filesystem directory to capture into.
      filename: File to store the stream
      sequence: ImageSequence proto.
      verbose: If True, print to screen.
      is_calibration: If True, this is a calibration sequence
    """
    raise NotImplementedError

  def StopStreaming(self):
    """Stop streaming.  Joins thread and waits for it to complete."""
    if self.streaming_thread is not None:
      self.stop_streaming = True
      self.streaming_thread.join()
    self.streaming_thread = None

  def StartCapture(self,
                   capture_dir,
                   filename,
                   sequence,
                   verbose=False,
                   is_calibration=False):
    """Threaded version of Capture that returns a Thread instance to join().

    Args:
      capture_dir: Filesystem directory to capture into.
      filename: File to capture into
      sequence: ImageSequence proto.
      verbose: If True, print to screen.
      is_calibration: If True, this is a calibration sequence

    Returns:
      Started Thread of Capture() routine.
    """
    cap_kwargs = {'capture_dir': capture_dir,
                  'filename': filename,
                  'sequence': sequence,
                  'verbose': verbose,
                  'is_calibration': is_calibration}
    t = threading.Thread(target=self.Capture, kwargs=cap_kwargs)
    t.start()
    return t

  def StartPreview(self, capture_dir, filename):
    """Threaded version of Capture that returns a Thread instance to join().

    Args:
      capture_dir: Filesystem directory to capture into.
      filename: File to capture into

    Returns:
      Started Thread of Capture() routine.
    """
    args = (capture_dir, filename)
    t = threading.Thread(target=self.Preview, args=args)
    t.start()
    return t

  def PrepareScan(self):
    """Checks that the camera is ready to begin the scan."""
    return True

  def Capture(self,
              capture_dir,
              filename,
              sequence,
              singleshot=False,
              verbose=False,
              preview=False,
              is_calibration=False):
    """Captures image into specified directory.

    Args:
      capture_dir: Filesystem directory to capture into.
      filename: Filename to capture to.
      sequence: ImageSequence proto.
      singleshot: True if the camera should only have one entry in the sequence
      verbose: If True, print to screen.
      preview: If True, this is a preview shot.
      is_calibration: If True, this is a calibration shot.

    Returns:
      Filename into which the capture was saved
    """
    raise NotImplementedError()

  def Preview(self):
    raise NotImplementedError

  def FillCameraInfo(self, camera_information):
    """Fills in CameraInformation proto.

    Subclasses must override.

    Args:
      camera_information: Camera information.
    """
    raise NotImplementedError

  def GetFormat(self):
    return swivel_scan_manifest_pb2.ScanImageSequence.JPEG

  def InitSequence(self, sequence):
    """Initializes metadata about this camera in sequence.

    Init does not occur if sequence is None or the camera is a PREVIEW
    camera.

    Args:
      sequence: Sequence proto.
    """
    if sequence is not None and self.position != PREVIEW:
      sequence.image_format = self.GetFormat()
      sequence.camera_position = self.position
      sequence.camera_inverted = self.inverted

      if self.angle_degrees:
        sequence.angle_degrees = self.angle_degrees

  def AppendSequence(self, sequence, filename, singleshot):
    """Appends capture to sequence.

    Append does not occur if sequence is None or the camera is a PREVIEW
    camera.

    Args:
      sequence: Sequence proto.
      filename: Filename of captured image.
      singleshot: If True, this is a single shot.
    """
    if sequence is not None and self.position != PREVIEW:
      # If the camera is a singleshot, we only want the filename to appear once.
      # TODO(arshan) this breaks the timestamps
      if singleshot and filename in sequence.filenames:
        return
      sequence.filenames.append(filename)
      sequence.timestamps.append(time.time())


class PrimesenseCamera(Camera):
  """Primesense/OpenNI controlled camera."""

  def __init__(self,
               guid=None,
               camera_number=100,
               rotate_degrees=0):
    super(PrimesenseCamera, self).__init__(
        position=swivel_scan_manifest_pb2.ScanImageSequence.DEPTH,
        camera_number=camera_number)
    self._driver = depth_camera.PrimesenseImpl(guid, rotate_degrees)
    self._rotate_degrees = rotate_degrees
    self._mutex = threading.RLock()

  def StartDriver(self):
    """Start driver."""
    self._driver.Start()

  def StopDriver(self):
    """Stop driver."""
    self._driver.Stop()

  @staticmethod
  def FromDict(raw_config):
    cam = PrimesenseCamera(guid=raw_config.get('guid', None),
                           rotate_degrees=raw_config.get('rotate_degrees', 0))
    FromDict(cam, raw_config)
    return cam

  def FillCameraInfo(self, camera_info):
    camera_info.id = self.inventory_id
    camera_info.camera_number = self.camera_number
    camera_info.description = 'PrimeSense OPENNI2-supported Sensor'

    if self._rotate_degrees in (90, 270):
      camera_info.image_width = 1024
      camera_info.image_height = 1280
    else:
      camera_info.image_width = 1280
      camera_info.image_height = 1024
    # Pixel sizes, focal length, etc. are not set, but these generally don't
    # matter for this application.
    camera_info.camera_type = (camera_information_pb2.
                               CameraInformation.PRIMESENSE_SENSOR)

  def GetFormat(self):
    return swivel_scan_manifest_pb2.ScanImageSequence.PNG

  def Stream(self,
             capture_dir,
             filename,
             sequence,
             verbose=False,
             is_calibration=False):
    if not os.path.exists(capture_dir):
      os.makedirs(capture_dir)
    path = os.path.join(capture_dir, filename)
    self._mutex.acquire()
    try:
      if verbose:
        print 'capturing to %s' % path
      if is_calibration:
        image = self._driver.Capture(True)
      else:
        images = []
        for _ in xrange(NUM_DEPTH_IMAGES_TO_AVERAGE):
          images.append(self._driver.Capture(False))
        image = depth_camera.AverageDepthImages(images)
        image = image.astype(images[0].dtype)

      self._driver.WriteToFile(image, path)
      self.AppendSequence(sequence, filename, False)
    finally:
      self._mutex.release()

  def Capture(self,
              capture_dir,
              filename,
              sequence=None,
              singleshot=False,
              verbose=False,
              preview=False,
              is_calibration=False):
    if not os.path.exists(capture_dir):
      os.makedirs(capture_dir)
    path = os.path.join(capture_dir, filename)
    self._mutex.acquire()
    try:
      if verbose:
        print 'capturing to %s' % path

      data = self._driver.Capture(is_calibration)
      self._driver.WriteToFile(data, path)

      self.AppendSequence(sequence, filename, singleshot)
    finally:
      self._mutex.release()
    return path


class WebCamera(Camera):
  """Webcam."""

  def __init__(self,
               port=None,
               position=swivel_scan_manifest_pb2.ScanImageSequence.FRONT,
               camera_number=100):
    super(WebCamera, self).__init__(position=position,
                                    camera_number=camera_number)
    self._port = port
    self._executor = executors.DefaultExecutor()

  @staticmethod
  def FromDict(raw_config):
    cam = WebCamera(raw_config.get('port', None))
    FromDict(cam, raw_config)
    return cam

  def FillCameraInfo(self, camera_info):
    camera_info.id = NOID
    camera_info.description = 'Unknown web camera'
    # TODO(kwc): need to derive these.
    # camera_info.image_width = 3000
    # camera_info.image_height = 2000

  def Capture(self,
              capture_dir,
              filename,
              sequence=None,
              singleshot=False,
              verbose=False,
              preview=False,
              is_calibration=False):
    if not os.path.exists(capture_dir):
      os.makedirs(capture_dir)
    path = os.path.join(capture_dir, filename)
    if verbose:
      print 'capturing to %s' % path
    if self._port:
      # Note: either have to check for regexp ourselves, or let the executor do
      # it.
      cmd = 'fswebcam -d %s %s' % (self._port, path)
      print cmd
      self._executor(cmd)
    else:
      self._executor('fswebcam %s' % path)
    self.AppendSequence(sequence, filename, singleshot)
    return path


# Drawing convenience
def DrawCrosshair(context, im, x, y, color, pixels=10):
  context.line((x, 0) + (x, im.size[1]), fill=color, width=pixels)
  context.line((0, y) + (im.size[0], y), fill=color, width=pixels)


def DrawGrid(context, im, grid_x, grid_y, color):
  step_x = im.size[0] / grid_x
  step_y = im.size[1] / grid_y

  # This isnt the cheapest way, but no pressure there.
  for x in range(1, grid_x):
    DrawCrosshair(context, im, step_x * x, step_y, color)
  for y in range(1, grid_y):
    DrawCrosshair(context, im, step_x, step_y * y, color)


# TODO(arshan): use the /main/settings/ownername to keep state on the position
# of the camera
# TODO(arshan): scan the usb bus and assign cameras based on the ownername
# (position)
class CanonCamera(Camera):
  """Canon camera."""

  def __init__(self, port=None, guid=None,
               position=swivel_scan_manifest_pb2.ScanImageSequence.FRONT,
               camera_number=100):
    super(CanonCamera, self).__init__(position, camera_number=camera_number)

    # Mutable for testing.
    self._executor = executors.DefaultExecutor()
    self._guid = None

    # Set the port, either by guid or by hardcoded ports.
    if guid is not None:
      self._port = None
      # self._guid = guid
      print 'Searching for guid %s' % guid

      command = 'gphoto2 --quiet --auto-detect'
      for gport in self._executor(command).split('\n'):
        m = re.search('(usb:[0-9,]+)', gport)
        if m:
          command = 'gphoto2 --quiet --port %s --get-config main/ownername' % m.group(1)
          if re.search(guid, self._executor(command)):
            self._port = m.group(1)
      if self._port is None:
        raise errors.ConfigError('Cannot find camera by guid : %s\n' % guid)
    else:
      self._port = port

    # Extra metadata fields.
    self._model = None
    self._aperture = 22
    self._shutterspeed = '1/20'
    self._iso = 100
    self._focal_length_mm = None
    # This is only used on the big rig station now.
    # TODO(bikas): move the setting and sizes into the yaml file.
    self._autocrop = False
    # Based on a desired image width of 4020 px
    self._crop_rect = (0, 0, 0, 0)
    self._rotate = 0

  @staticmethod
  def FromDict(raw_config):
    """Creates new instances from dictionary.

    Args:
      raw_config: Configuration in dict representation.
    """
    if 'guid' in raw_config:
      camera = CanonCamera(guid=raw_config['guid'])
      FromDict(camera, raw_config)
    else:
      camera = CanonCamera(port=raw_config['port'])
      FromDict(camera, raw_config)

    camera._model = raw_config['model']
    supported = [CANON_REBEL_T2I, CANON_REBEL_T4I, CANON_EOS_5DM2, CANON_EOS_5DM3]
    if not camera._model in supported:
      raise errors.ConfigError('Unknown/unsupported camera model: %s.\n'
                               'Supported types are: %s' %
                               (camera._model, ','.join(supported)))

    if 'iso' in raw_config:
      camera._iso = int(raw_config['iso'])
    if 'shutterspeed' in raw_config:
      camera._shutterspeed = raw_config['shutterspeed']
    if 'aperture' in raw_config:
      camera._aperture = float(raw_config['aperture'])
    if 'focal_length_mm' in raw_config:
      camera._focal_length_mm = float(raw_config['focal_length_mm'])
    if 'angle_degrees' in raw_config:
      camera.angle_degrees = int(raw_config['angle_degrees'])
    if 'crop_rectangle' in raw_config:
      camera.SetCrop(ast.literal_eval(raw_config['crop_rectangle']))
    if 'rotate_degrees' in raw_config:
      camera.SetRotate(int(raw_config['rotate_degrees']))

    return camera

  def SetCrop(self, crop_rectangle):
    """Enable and set the cropping rectangle for this camera."""
    self._crop_rect = crop_rectangle
    self._autocrop = True
    print ('Crop rectangle: %r' % (self._crop_rect,))

  def SetRotate(self, rotate_degrees):
    """Enable and set the rotation applied to the image post-capture."""
    print 'Setting image rotation: %d' % rotate_degrees
    self._rotate = rotate_degrees

  def FindPort(self, guid):
    print ('Searching for guid %s' % guid)

    command = 'gphoto2 --quiet --auto-detect'
    for gport in self._executor(command).split('\n'):
      m = re.search('(usb:[0-9,]+)', gport)
      if m:
        command = 'gphoto2 --quiet --port %s --get-config main/ownername' % m.group(1)
        if re.search(guid, self._executor(command)):
          return m.group(1)
    if self._port == None:
      raise errors.ConfigError('Cannot find camer by guid : %s\n' % guid)

  def PrepareScan(self):
    """Check if the camera is ready to scan.

    If the guid doesn't match what the camera is try
    to grab the correct camera.
    """
    # return True
    if not self._guid == None:
      command = 'gphoto2 --quiet --port %s --get-config main/ownername' % self._port
      if not re.search(self._guid, self._executor(command)):
        print('Camera guid port mapping changed')
        self._port = self.FindPort(self._guid)
        # TODO(willmartin): Make this actually check if the camera was adressed correctly.
        return True
      else:
        return True
    else:
      return True

  def FillCameraInfo(self, camera_info):
    """Fill CameraInfo proto with this camera's metadata.

    Args:
      camera_info: CameraInfo instance.
    """
    if not self.inventory_id:
      raise errors.ConfigError('Cannot fill CameraInfo: inventory id is not set')
    camera_info.id = self.inventory_id
    camera_info.camera_number = self.camera_number
    if self._model:
      camera_info.description = self._model
    if self._focal_length_mm:
      camera_info.focal_length_mm = self._focal_length_mm
    if self._aperture:
      camera_info.f_stop = self._aperture

    # TODO(jarussell): It would be far more robust to obtain these resolutions
    # from the camera_server or gphoto rather than hard coding them here.
    camera_info.image_width = 5184
    camera_info.image_height = 3456
    if self._model == CANON_REBEL_T2I:
      camera_info.camera_type = (
        camera_information_pb2.CameraInformation.CANON_REBEL_T2I)
    elif self._model == CANON_REBEL_T4I:
      camera_info.camera_type = (
        camera_information_pb2.CameraInformation.CANON_REBEL_T4I)
    elif self._model == CANON_EOS_5DM2:
      camera_info.image_width = 5616
      camera_info.image_height = 3744
      camera_info.camera_type = (
        camera_information_pb2.CameraInformation.CANON_EOS_5DM2)
    elif self._model == CANON_EOS_5DM3:
      camera_info.image_width = 5760
      camera_info.image_height = 3840
      camera_info.camera_type = (
        camera_information_pb2.CameraInformation.CANON_EOS_5DM3)

    if self._autocrop:
      camera_info.image_width = self._crop_rect[2] - self._crop_rect[0]
      camera_info.image_height = self._crop_rect[3] - self._crop_rect[1]

    # TODO(kwc): need to derive these.
    #camera_info.pixel_width = 1.0
    #camera_info.pixel_height = 1.0
    #camera_info.pixel_height_um = 1.0

  def Preview(self, capture_dir, filename):
    path = self.Capture(capture_dir, filename, None, False, False, True)
    # We are acting on the fullsize image ... how slow will that be?
    im = Image.open(path)
    context = ImageDraw.Draw(im)
    # centerX = im.size[0] / 2
    # centerY = im.size[1] / 2
    DrawGrid(context, im, 8, 6, '#22AA22')

    im.save(path)
    return path

  def PostProcess(self, file_path):
    """Execute any post image capture processes. """
    if self._autocrop or self._rotate != 0:
      im = Image.open(file_path)
      if self._rotate != 0:
        print 'rotating img: %d' % self._rotate
        im = im.rotate(self._rotate)
      if self._autocrop:
        im = im.crop(self._crop_rect)
      im.save(file_path, 'JPEG', quality=98)

  # Will this work with the Capture action? no dir/filename ...
  def Capture(self, capture_dir, filename, sequence=None,
              singleshot=False, verbose=False, preview=False,
              is_calibration=False):
    if not os.path.exists(capture_dir):
      os.makedirs(capture_dir)

    path = os.path.join(capture_dir, filename)
    print 'capturing to %s' % path
    # TODO(arshan): bind to the gphoto-lib instead
    command = ('gphoto2 --port %s --set-config " / main / imgsettings / iso= % d" --set-config " / main / capturesettings / aperture= % d" --set-config " / main / capturesettings / shutterspeed= % s" --filename=%s --force-overwrite ' %
               (self._port, self._iso, self._aperture, self._shutterspeed, path))
    if (preview):
      # would be good, but the preview mode is generating some weird data file right now?
      # command += '--capture-preview'
      command += '--capture-image-and-download'
    else:
      command += '--capture-image-and-download'
    print command
    self._executor(command)
    if (self._autocrop):
      im = Image.open(path)
      im.crop(self._crop_rect).save(path, 'JPEG', quality=98)
    self.AppendSequence(sequence, filename, singleshot)
    #if (preview):
      # gphoto ignores the --filename option when the --capture-preview option is used.
      # TODO(arshan): Wrap the lib and make the c calls instead of shelling out.
      #shutil.move('preview.jpg', path)
    return path


class ArtProjectCamera(CanonCamera):
  """ Access to Canon cameras using the ArtProjectServer.
  Assumes that your already running the server, which controls the camera.
  Known to work with the 5Dm3."""

  def __init__(self, port=None, guid=None,
               position=swivel_scan_manifest_pb2.ScanImageSequence.FRONT,
               camera_number=100, url='localhost:8090'):

    super(ArtProjectCamera, self).__init__(position, camera_number=camera_number)

    # Mutable for testing.
    self._executor = executors.DefaultExecutor()

    # Set default values
    self._model = None
    self._aperture = 22
    self._shutterspeed = '1/20'
    self._iso = 100
    self._focal_length_mm = None
    self._autocrop = False
    self._crop_rect = (0, 0, 0, 0)
    self._server_url = url

  @staticmethod
  def FromDict(raw_config):
    """Creates new instances from dictionary.

    Args:
      raw_config: Configuration in dict representation.
    """
    camera = ArtProjectCamera(url=raw_config['server_url'])
    FromDict(camera, raw_config)

    camera._model = raw_config['model']
    supported = [CANON_EOS_5DM3]

    if not camera._model in supported:
      raise errors.ConfigError('Unknown/unsupported camera model: %s.\n'
                               'Supported types are: %s' %
                               (camera._model, ','.join(supported)))

    if 'iso' in raw_config:
      camera._iso = int(raw_config['iso'])
    if 'shutterspeed' in raw_config:
      camera._shutterspeed = raw_config['shutterspeed']
    if 'aperture' in raw_config:
      camera._aperture = float(raw_config['aperture'])
    if 'focal_length_mm' in raw_config:
      camera._focal_length_mm = float(raw_config['focal_length_mm'])
    if 'angle_degrees' in raw_config:
      camera.angle_degrees = int(raw_config['angle_degrees'])
    if 'crop_rectangle' in raw_config:
      camera.SetCrop(ast.literal_eval(raw_config['crop_rectangle']))
    if 'rotate_degrees' in raw_config:
      camera.SetRotate(int(raw_config['rotate_degrees']))

    return camera

  def PrepareScan(self):
    return True

  def Capture(self, capture_dir, filename, sequence=None, singleshot=False, verbose=False, preview=False, is_calibration=False):
    path = os.path.join(capture_dir, filename)
    command = ('wget %s/image --output-document %s' % (self._server_url, path))

    print command
    self._executor(command)
    self.PostProcess(path)
    self.AppendSequence(sequence, filename, singleshot)

    return path


class FakeCamera(Camera):

  def __init__(self, size,
               position=swivel_scan_manifest_pb2.ScanImageSequence.FRONT,
               camera_number=100):
    super(FakeCamera, self).__init__(position=position,
                                     camera_number=camera_number)
    self._size = size

    # FakeCamera doesn't need an executor, but this is used as a test hook to
    # signal no side effects.
    self._executor = None

  @staticmethod
  def FromDict(raw_config):
    width = raw_config['width']
    height = raw_config['height']

    camera = FakeCamera((width, height))
    FromDict(camera, raw_config)
    return camera

  def FillCameraInfo(self, camera_info):
    camera_info.id = NOID
    camera_info.camera_number = self.camera_number
    camera_info.description = 'PIL-generated image'
    camera_info.image_width = self._size[0]
    camera_info.image_height = self._size[1]

  def Capture(self, capture_dir, filename, sequence=None, singleshot=False, verbose=False, is_calibration=False):
    path = os.path.join(capture_dir, filename)
    if verbose:
      print '[fake]-capturing to %s' % path

    im = Image.new('RGB', self._size, (255, 0, 0))
    if self._executor is None:
      if not os.path.exists(capture_dir):
        os.makedirs(capture_dir)
      im.save(path, 'jpeg')
    elif isinstance(self._executor, executors.MockExecutor):
      self._executor('fake-save ^%s' % path)
    else:
      raise errors.InternalError('Unexpected use of executor.')

    self.AppendSequence(sequence, filename, singleshot)
    return path
