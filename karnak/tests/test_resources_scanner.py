# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for resources.scanner."""
__author__ = "kwc@google.com (Ken Conley)"

import os
import shutil
import tempfile
import time

import mock

from model import swivel_scan_manifest_pb2
import resources
from resources import camera
from resources import crosshair
from resources import errors
from resources import executors
from resources import lighting
from resources import packer
from resources import scanner
from resources import scanner_config
from resources import station
from resources import stepper
from resources import storage


class MockStation(object):

  def __init__(self, id):
    self.name = id
    self.base_directory = tempfile.gettempdir()
    self.capture_directory = tempfile.gettempdir()
    self.calibration_directory = tempfile.gettempdir()


class MockScannerConfig(object):

  def __init__(self):
    self.packer = None
    self.station = MockStation("Station 1")

  def GetResource(self, name):
    return None

  def GetResourceNames(self):
    return []


def test_OrthoTable():
  s = scanner.OrthoTable()
  assert s.camera is None
  try:
    s.StartScan("fake-request")
    assert False, "Should have raised"
  except errors.InternalError:
    pass


def GetOrthoTableDict():
  return dict(
      name="Ortho Scanner 1", resources=["fake_camera", "fake_2d"], 
      type="OrthoTable", table_type="GLASS")


def test_OrthoTable_FromDict():
  d = GetOrthoTableDict()
  s = scanner.OrthoTable.FromDict(d)
  assert d["name"] == s.name
  assert d["name"] in str(s)
  assert d == s.raw_config
  assert d["resources"] == s._resource_names
  assert s.camera is None
  assert s.table_type is swivel_scan_manifest_pb2.ScanImageSequence.GLASS


def test_OrthoTable_Factory_FromDict():
  d = GetOrthoTableDict()
  factory = resources.DefaultFactory()
  s = factory.CreateFromDict(d)
  assert isinstance(s, scanner.OrthoTable)


def test_OrthoTable_InitFail():
  d = GetOrthoTableDict()
  s = scanner.OrthoTable.FromDict(d)
  try:
    s.Init(MockScannerConfig())
    assert False, "Should have raised"
  except errors.ConfigError:
    pass


def test_OrthoTable_Scan():
  tmpdir = tempfile.mkdtemp()
  try:
    d = GetOrthoTableDict()
    s = scanner.OrthoTable.FromDict(d)
    config = GetFakeConfig(tmpdir)
    s.Init(config)

    # Disable prepare scan as it requires physical files.
    def Noop(*args): pass
    s.PrepareScan = Noop

    retval = s.StartScan()
    # capture_directory should be non-empty, but not contain any path separators
    # as basedir == capture dir.
    assert retval["capture_directory"], retval["capture_directory"]
    assert os.pathsep not in retval["capture_directory"], retval["capture_directory"]
    capture_dir = os.path.join(tmpdir, retval["capture_directory"])
    assert "scanning" == retval["status"]

    retval = s.StopScan()
    assert "halted" == retval["status"]

    # Verify the serialized manifest.
    timeout = time.time() + 1.
    manifest_path = os.path.join(capture_dir, scanner.MANIFEST_FILENAME)
    while not os.path.isfile(manifest_path) and time.time() < timeout:
      time.sleep(0.01)
    assert os.path.exists(capture_dir)
    deser_manifest = swivel_scan_manifest_pb2.ScanObject()
    with open(manifest_path, "r") as f:
      deser_manifest.ParseFromString(f.read())
    assert len(deser_manifest.image_sequences) == 1
    assert len(deser_manifest.image_sequences[0].filenames) == 1
  finally:
    shutil.rmtree(tmpdir)


def test_OrthoTable_Scan_Empty():
  d = GetOrthoTableDict()
  s = scanner.OrthoTable.FromDict(d)
  config = GetFakeConfig()
  s.Init(config)

  # Disable prepare scan as it requires physical files.
  def Noop(*args): pass
  s.PrepareScan = Noop

  retval = s.StartScan(capture_type=scanner.CAPTURE_TYPE_EMPTY)
  assert "capture_directory" in retval
  assert "scanning" == retval["status"]

  retval = s.StopScan()
  assert "halted" == retval["status"]


def test_OrthoTable_Scan_Calibration():
  d = GetOrthoTableDict()
  s = scanner.OrthoTable.FromDict(d)
  config = GetFakeConfig()
  s.Init(config)

  # Disable prepare scan as it requires physical files.
  def Noop(*args): pass
  s.PrepareScan = Noop

  retval = s.StartScan(capture_type=scanner.CAPTURE_TYPE_CALIBRATION)
  assert "capture_directory" in retval
  assert "scanning" == retval["status"]

  retval = s.StopScan()
  assert "halted" == retval["status"]


def test_Scanner2d():
  s = scanner.Scanner2d()
  assert s.turntable is None
  try:
    s.StartScan("fake-kid")
    assert False, "Should have raised"
  except errors.InternalError:
    pass


def GetScanner2dDict():
  return dict(
      name="Scanner 1", resources=["fake_camera", "turntable"],
      scan_segments=100,
      type="Scanner2d",
      table_type="WHITE_WOOD")


def test_CreateManifest():
  config = scanner_config.ScannerConfig()
  config.station = station.Station()
  config.station.name = "my station"
  config.station.model = "some model id"
  m = scanner.CreateManifest(config, "K5678")
  assert m.katamari_id == "K5678"
  assert m.scan_station.id == "my station"
  assert m.scan_station.model_id == "some model id"


def test_Scanner2d_FromDict():
  d = GetScanner2dDict()
  s = scanner.Scanner2d.FromDict(d)
  assert d["name"] == s.name
  assert d["name"] in str(s)
  assert d == s.raw_config
  assert d["scan_segments"] == s.scan_segments
  assert d["resources"] == s._resource_names
  assert s.resources is None
  assert s.table_type is swivel_scan_manifest_pb2.ScanImageSequence.WHITE_WOOD


def test_Scanner2d_Factory_FromDict():
  d = GetScanner2dDict()
  factory = resources.DefaultFactory()
  s = factory.CreateFromDict(d)
  assert isinstance(s, scanner.Scanner2d)


def test_Scanner2d_InitFail():
  d = GetScanner2dDict()
  s = scanner.Scanner2d.FromDict(d)
  try:
    s.Init(MockScannerConfig())
    assert False, "Should have raised"
  except errors.ConfigError:
    pass


def test_Scanner2d_StopScan_NoScan():
  d = GetScanner2dDict()
  s = scanner.Scanner2d.FromDict(d)
  retval = s.StopScan()
  assert "no current scan" == retval["status"]


def GetFakeConfig(tmpdir=None):
  if tmpdir is None:
    tmpdir = tempfile.gettempdir()
  config = scanner_config.ScannerConfig()
  fake_camera = camera.FakeCamera((10, 10))
  fake_camera._executor = executors.MockExecutor()
  fake_camera.name = "fake_camera"
  fake_2d = mock.MagicMock(scanner.Scanner2d)
  fake_2d.name = "fake_2d"
  config.packer = packer.Tarball(tmpdir)
  config.resources.append(fake_camera)
  config.resources.append(fake_2d)
  config.station = station.Station()
  config.station.name = "fake_station"
  config.base_directory = tmpdir
  config.station.capture_directory = tmpdir
  config.station.calibration_directory = tmpdir
  turntable = stepper.FakeStepper()
  turntable.name = "turntable"
  config.resources.append(turntable)
  return config


def test_Scanner2d_Scan():
  d = GetScanner2dDict()
  s = scanner.Scanner2d.FromDict(d)
  config = GetFakeConfig()
  s.Init(config)

  # TODO(kwc): need to test scanning where we pass in a capture_directory to
  # resume from.
  controller = mock.MagicMock(scanner.Scan2dController)
  retval = s.StartScan(controller=controller)
  assert "capture_directory" in retval
  assert "scanning" == retval["status"]

  retval = s.StopScan()
  assert "halted" == retval["status"]


def test_Scanner2d_Scan_Empty():
  d = GetScanner2dDict()
  s = scanner.Scanner2d.FromDict(d)
  config = GetFakeConfig()
  s.Init(config)

  # TODO(kwc): need to test scanning where we pass in a capture_directory to
  # resume from.
  controller = mock.MagicMock(scanner.Scan2dController)
  retval = s.StartScan(controller=controller,
                       capture_type=scanner.CAPTURE_TYPE_EMPTY)
  assert "capture_directory" in retval
  assert "scanning" == retval["status"]

  retval = s.StopScan()
  assert "halted" == retval["status"]


def test_Scanner2d_Scan_Calibration():
  d = GetScanner2dDict()
  s = scanner.Scanner2d.FromDict(d)
  config = GetFakeConfig()
  s.Init(config)

  # TODO(kwc): need to test scanning where we pass in a capture_directory to
  # resume from.
  controller = mock.MagicMock(scanner.Scan2dController)
  retval = s.StartScan(controller=controller,
                       capture_type=scanner.CAPTURE_TYPE_CALIBRATION)
  assert "capture_directory" in retval
  assert "scanning" == retval["status"]

  retval = s.StopScan()
  assert "halted" == retval["status"]


class MockTurntable(object):
  def SetSegments(self):
    pass


def test_Scan2dController_PrepareController():
  manifest = swivel_scan_manifest_pb2.ScanObject()
  s = mock.MagicMock(scanner.Scanner2d)
  s.table_type = swivel_scan_manifest_pb2.ScanImageSequence.GLASS
  s.scan_segments = 100
  s.starting_rotation_angle = 90
  s.turntable = mock.MagicMock(stepper.ImsStepperWrapper)
  s.config = mock.MagicMock(scanner_config.ScannerConfig)
  s.config.packer = mock.MagicMock(packer.Tarball)
  s.config.station = MockStation("Station 1")
  s.resources = [camera.WebCamera(), camera.WebCamera()]
  controller = scanner.Scan2dController(s, manifest, tempfile.gettempdir())

  start = time.time()
  front, top, ortho = controller.PrepareController()
  assert s.resources == [x[0] for x in front]
  assert [] == ortho
  assert [] == top
  manifest = controller.manifest
  assert start <= manifest.capture_time_start
  assert len(manifest.image_sequences) == len(s.resources)


def test_ScannerController_Run():
  # TODO(kwc): real temp dir logic
  tmpdir = tempfile.mkdtemp()
  manifest_path = os.path.join(tmpdir, scanner.MANIFEST_FILENAME)
  try:
    manifest = swivel_scan_manifest_pb2.ScanObject()
    manifest.katamari_id = "K0000000000"
    kid = manifest.katamari_id
    s = mock.MagicMock(scanner.Scanner2d)
    # TODO(kwc): use callback to improve test.
    s.scan_callback = None
    s.scan_segments = 72
    s.starting_rotation_angle = 90
    s.table_type = swivel_scan_manifest_pb2.ScanImageSequence.GLASS
    s.config = mock.MagicMock(scanner_config.ScannerConfig)
    s.config.packer = mock.MagicMock(packer.Tarball)
    s.config.station = MockStation("Station 1")
    s.crosshair = mock.MagicMock(crosshair.Crosshair)
    s.lighting = mock.MagicMock(lighting.LightingController)
    fake_output = "fake_output"
    fake_asset_id = "fake_asset_id"
    s.config.packer.GetSwivelAssetId.return_value = fake_asset_id
    s.config.packer.Create.return_value = fake_output
    s.config.storage = [mock.MagicMock(storage.BigStore)]
    s.turntable = mock.MagicMock(stepper.ImsStepperWrapper)
    ports = ["/fake/port-0", "/fake/port-1"]
    s.resources = [
        camera.WebCamera(ports[0], scanner.FRONT, 10),
        camera.WebCamera(ports[1], scanner.TOP, 20),
        ]
    for i, c in enumerate(s.resources):
      c._executor = executors.MockExecutor()
      c.name = "resource-%d" % i
    controller = scanner.Scan2dController(s, manifest, tmpdir)
    start = time.time()
    controller.Run(verbose=False)

    # Check calls into resources.
    # Camera captures.
    assert 2 == len(manifest.image_sequences)
    front_seq = [seq for seq in manifest.image_sequences
                 if seq.camera_position == scanner.FRONT][0]
    assert 5 == front_seq.angular_increment_degrees
    top_seq = [seq for seq in manifest.image_sequences
               if seq.camera_position == scanner.TOP][0]
    assert 90 == top_seq.angular_increment_degrees, "%s %s %s" % (str(top_seq),
        controller._GetAngularIncrement(top_seq), controller.capture_type)
    expected = ["10-%03d.jpg" % deg for deg in range(0, 360, 5)]
    assert front_seq.filenames == expected
    expected = ["20-%03d.jpg" % deg for deg in range(0, 360, 90)]
    assert list(top_seq.filenames) == expected, "%s vs. %s" % (list(top_seq.filenames), expected)
    # - Turntable spins.
    s.turntable.SetSegments.assert_called_with(s.scan_segments)
    assert s.scan_segments - 1 == s.turntable.StepOneSegment.call_count
    # - Uploader.
    store = s.config.storage[0]
    store.UploadFiles.assert_called_with(kid,
                                         [fake_output, manifest_path])

    # Check manifest metadata.
    assert start < manifest.capture_time_start
    assert manifest.capture_time_start < manifest.capture_time_end
    assert manifest.capture_time_end <= time.time()

    # Verify the serialized manifest.
    deser_manifest = swivel_scan_manifest_pb2.ScanObject()
    with open(manifest_path, "r") as f:
      deser_manifest.ParseFromString(f.read())
      assert manifest == deser_manifest
  finally:
    shutil.rmtree(tmpdir)


def testInitSequence():
  mock_camera = mock.MagicMock(camera.CanonCamera)
  mock_camera.camera_number = 10
  mock_scanner = mock.MagicMock(scanner.Scanner2d)
  mock_scanner.table_type = scanner.TABLE_MAP["GLASS"]
  mock_scanner.starting_rotation_angle = 90
  seq = swivel_scan_manifest_pb2.ScanImageSequence()
  scanner.InitSequence(mock_camera, seq, mock_scanner, 15)
  assert mock_scanner.starting_rotation_angle == seq.starting_rotation_angle_degrees
  assert 15 == seq.angular_increment_degrees
  mock_camera.FillCameraInfo.assert_called_with(seq.camera_information)
  mock_camera.InitSequence.assert_called_with(seq)
