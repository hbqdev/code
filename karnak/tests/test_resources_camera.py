# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for resources.camera."""
__author__ = "kwc@google.com (Ken Conley)"

import os
import tempfile
import time

from model import swivel_scan_manifest_pb2
import resources
from resources import camera
from resources import executors

FRONT = swivel_scan_manifest_pb2.ScanImageSequence.FRONT
TOP = swivel_scan_manifest_pb2.ScanImageSequence.TOP
ORTHO = swivel_scan_manifest_pb2.ScanImageSequence.ORTHO

# TODO(kwc): this test is dirty and does not cleanup temp files.


def testCamera_abstract():
  c = camera.Camera()
  c.Init('ignore')
  assert swivel_scan_manifest_pb2.ScanImageSequence.FRONT == c.position
  seq = swivel_scan_manifest_pb2.ScanImageSequence()
  filename = 'foo.jpg'
  try:
    c.Capture(tempfile.gettempdir(), filename, seq)
  except NotImplementedError:
    pass
  try:
    c.FillCameraInfo(seq.camera_information)
  except NotImplementedError:
    pass


def testCamera_AppendSequence_None():
  c = camera.Camera()
  c.Init('ignore')
  c.AppendSequence(None, 'foo.jpg')


def testCamera_AppendSequence():
  position = swivel_scan_manifest_pb2.ScanImageSequence.TOP
  c = camera.Camera(position=position)
  c.Init('ignore')
  seq = swivel_scan_manifest_pb2.ScanImageSequence()
  start = time.time()
  c.AppendSequence(seq, 'foo.jpg')
  assert 1 == len(seq.filenames)
  assert'foo.jpg' == seq.filenames[0]
  assert 1 == len(seq.timestamps)
  assert seq.timestamps[0] > start
  assert seq.timestamps[0] < time.time()


def testCamera_InitSequence():
  position = swivel_scan_manifest_pb2.ScanImageSequence.TOP
  c = camera.Camera(position=position)
  c.Init('ignore')
  seq = swivel_scan_manifest_pb2.ScanImageSequence()

  def FakeFill(*args): pass
  c.FillCameraInfo = FakeFill
  c.InitSequence(seq)
  assert position == seq.camera_position
  assert not seq.HasField('angle_degrees')
  assert 0 == len(seq.filenames)
  assert 0 == len(seq.timestamps)


def testCamera_InitSequence_AngleDegrees():
  c = camera.Camera(angle_degrees=1)
  c.Init('ignore')
  seq = swivel_scan_manifest_pb2.ScanImageSequence()

  def FakeFill(*args): pass
  c.FillCameraInfo = FakeFill
  c.InitSequence(seq)
  assert 1 == seq.angle_degrees


def testCamera_AppendSequence_PREVIEW():
  c = camera.Camera(position=camera.PREVIEW)
  c.Init('ignore')
  seq = swivel_scan_manifest_pb2.ScanImageSequence()

  c.AppendSequence(seq, 'foo.jpg')
  assert not seq.filenames


def testWebCamera_FromDict_NotInverted():
  d = dict(type="WebCamera", name="Camera 1",
           camera_number=10, position="FRONT")
  c = camera.WebCamera.FromDict(d)
  assert isinstance(c, camera.WebCamera)
  assert FRONT == c.position, c.position
  assert 10 == c.camera_number, c.camera_number
  assert "Camera 1" == c.name
  assert d == c.raw_config, "%s vs %s" % (d, c.raw_config)
  assert not c.inverted


def testWebCamera_FromDict_Inverted():
  d = dict(type="WebCamera", name="Camera 1", inverted=True,
           camera_number=10, position="FRONT")
  c = camera.WebCamera.FromDict(d)
  assert c.inverted


def testWebCamera_Factory_FromDict():
  d = dict(type="WebCamera", name="Camera 1",
           camera_number=10, position="FRONT")
  factory = resources.DefaultFactory()
  c = factory.CreateFromDict(d)
  assert isinstance(c, camera.WebCamera)


def testWebCamera_FromDictFail():
  d = dict(name="Camera 1", position="FRONT")
  try:
    camera.WebCamera.FromDict(d)
    assert False, "Should have raised"
  except KeyError:
    pass


def testWebCamera_FillCameraInfo():
  d = dict(name="Camera 1", camera_number=10, position="FRONT")
  c = camera.WebCamera.FromDict(d)
  camera_info = swivel_scan_manifest_pb2.CameraInformation()
  c.FillCameraInfo(camera_info)
  # WebCamera doesn"t have valid fields, just make sure they are there.
  assert camera_info.id
  assert camera_info.description
  camera_info.SerializeToString()


def _test_Capture(c, verify_command):
  c._executor = executors.MockExecutor()
  angles = range(0, 360, 5)
  sequence = swivel_scan_manifest_pb2.ScanImageSequence()
  d = tempfile.gettempdir()
  for step, angle in enumerate(angles):
    filename = "capture-%d.jpg" % (step)
    c.Capture(d, filename, sequence)

    expected_path = os.path.join(d, filename)
    verify_command(c._executor.last_command)
    assert expected_path in c._executor.last_command

    assert sequence.filenames[-1] == filename
    assert sequence.timestamps[-1] < time.time()
    assert len(sequence.filenames) == step + 1
    assert len(sequence.timestamps) == step + 1


def testWebCamera_Capture():

  def CheckCommand(command):
    pass

  d = dict(name="Camera 1", camera_number=10, position="FRONT")
  c = camera.WebCamera.FromDict(d)
  _test_Capture(c, CheckCommand)


def _GetFakeCameraDict():
  return dict(
      type="FakeCamera", name="Camera 1",
      camera_number=10, position="FRONT",
      width=640, height=480)


def testFakeCamera_FromDict():
  d = _GetFakeCameraDict()
  c = camera.FakeCamera.FromDict(d)
  assert FRONT == c.position, c.position
  assert 10 == c.camera_number, c.camera_number
  assert "Camera 1" == c.name
  assert d == c.raw_config, "%s vs %s" % (d, c.raw_config)


def testFakeCamera_Factory_FromDict():
  d = _GetFakeCameraDict()
  factory = resources.DefaultFactory()
  c = factory.CreateFromDict(d)
  assert isinstance(c, camera.FakeCamera)


def testFakeCamera_FromDictFail():
  d = _GetFakeCameraDict()
  del d["width"]
  try:
    camera.FakeCamera.FromDict(d)
    assert False, "Should have raised"
  except KeyError:
    pass


def testFakeCamera_FillCameraInfo():
  d = _GetFakeCameraDict()
  c = camera.FakeCamera.FromDict(d)
  camera_info = swivel_scan_manifest_pb2.CameraInformation()
  c.FillCameraInfo(camera_info)
  # FakeCamera doesn"t have valid fields, just make sure they are there.
  assert camera_info.id
  assert camera_info.description
  camera_info.SerializeToString()


def testFakeCamera_Capture_Real():
  try:
    import Image
  except ImportError:
    assert False, "PIL is not installed, cannot test actual FakeCamera capture"
  d = _GetFakeCameraDict()
  c = camera.FakeCamera.FromDict(d)

  filename = None
  try:
    tmp_dir = tempfile.gettempdir()
    seq = swivel_scan_manifest_pb2.ScanImageSequence()
    filename = "capture.jpg"
    c.Capture(tmp_dir, filename, seq)
    filename = os.path.join(tmp_dir, filename)

    assert os.path.isfile(filename), filename
  finally:
    if filename and os.path.isfile(filename):
      os.remove(filename)

def testFakeCamera_Capture():

  def CheckCommand(command):
    pass

  d = _GetFakeCameraDict()
  c = camera.FakeCamera.FromDict(d)
  _test_Capture(c, CheckCommand)


def _DefaultCanonCameraDict(model=None):
  if model is None:
    model = camera.CANON_REBEL_T2I
  d = {
      "type": "CanonCamera",
      "camera_number": 20,
      "position": "TOP",
      "inventory_id": "Fake inventory id",
      "model": model,
      "name": "The Camera",
      "port": "usb:002,003",
      "inverted": True,
      "focal_length_mm": 50.,
      "aperture": 18,
      "shutterspeed": 1/13,
      "iso": 100,
      }
  return d


def testCanonCamera_FromDict():
  d = _DefaultCanonCameraDict()
  c = camera.CanonCamera.FromDict(d)
  assert d == c.raw_config
  assert "The Camera" == c.name
  assert TOP == c.position, c.position
  assert d["camera_number"] == c.camera_number, c.camera_number
  assert d["port"] == c._port, c._port
  assert d["model"] == c._model, c._model
  assert d["aperture"] == c._aperture, c._aperture
  assert d["iso"] == c._iso, c._iso
  assert d["focal_length_mm"] == c._focal_length_mm, c._focal_length_mm


def testCanonCameraT4i_FromDict():
  # Tripwire.  Main tests is FillCameraInformation.
  d = _DefaultCanonCameraDict(model=camera.CANON_REBEL_T4I)
  c = camera.CanonCamera.FromDict(d)
  assert d["model"] == c._model, c._model


def testCanonCamera_Factory_FromDict():
  d = _DefaultCanonCameraDict()
  factory = resources.DefaultFactory()
  c = factory.CreateFromDict(d)
  assert isinstance(c, camera.CanonCamera)


def testCanonCamera_FromDictFail():
  d = dict(camera_number=10, position="FRONT")
  try:
    camera.CanonCamera.FromDict(d)
    assert False, "Should have raised"
  except KeyError:
    pass


def testCanonCamera_FillCameraInfo():
  d = _DefaultCanonCameraDict()
  c = camera.CanonCamera.FromDict(d)
  camera_info = swivel_scan_manifest_pb2.CameraInformation()
  c.FillCameraInfo(camera_info)
  assert d["inventory_id"] == camera_info.id
  assert d["model"] == camera_info.description
  assert d["aperture"] == camera_info.f_stop
  assert d["focal_length_mm"] == camera_info.focal_length_mm
  assert (swivel_scan_manifest_pb2.CameraInformation.CANON_REBEL_T2I ==
          camera_info.camera_type)
  camera_info.SerializeToString()


def testCanonCameraT4I_FillCameraInfo():
  d = _DefaultCanonCameraDict(model=camera.CANON_REBEL_T4I)
  c = camera.CanonCamera.FromDict(d)
  camera_info = swivel_scan_manifest_pb2.CameraInformation()
  c.FillCameraInfo(camera_info)
  assert (swivel_scan_manifest_pb2.CameraInformation.CANON_REBEL_T4I ==
          camera_info.camera_type)
  camera_info.SerializeToString()


def testCanonCamera_Capture():
  d = _DefaultCanonCameraDict()
  d['position'] = 'ORTHO'
  d['angle_degrees'] = 10
  c = camera.CanonCamera.FromDict(d)

  def CheckCommand(command):
    assert c._port in command

  _test_Capture(c, CheckCommand)
