# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests resources.scanner_config."""
__author__ = "kwc@google.com (Ken Conley)"

import os

import resources
from resources import camera
from resources import errors
from resources import lighting
from resources import packer
from resources import scanner_config
from resources import stepper
from tests import mock_hardware

TEST_FILE = "test_resources_scanner_config.yaml"
TEST_FILE_NON_DICT = "test_resources_scanner_config_nondict.yaml"

mock_hardware.MockAll()


def GetResourcePath():
  return os.path.dirname(__file__)


def testLoadConfigFromFile_NoFile():
  factory = resources.DefaultFactory()
  try:
    scanner_config.LoadConfigFromFile('not a file', factory)
    assert False, "Should have raised"
  except errors.ConfigError:
    pass


def testLoadConfigFromFile_NonDict():
  factory = resources.DefaultFactory()
  test_file = os.path.join(GetResourcePath(), TEST_FILE_NON_DICT)
  try:
    scanner_config.LoadConfigFromFile(test_file, factory)
    assert False, "Should have raised"
  except errors.ConfigError:
    pass


def testLoadConfigFromFile():
  factory = resources.DefaultFactory()
  test_file = os.path.join(GetResourcePath(), TEST_FILE)
  c = scanner_config.LoadConfigFromFile(test_file, factory)
  assert c is not None
  assert c.credentials
  assert c.station
  assert "Station Name" == c.station.name
  assert c.station.touchscreen
  assert "Revision 2012/07; lights:20120807_cross2_top6" == c.station.model
  assert isinstance(c.packer, packer.Tarball)
  assert "tarballs" == c.packer._output_dir

  assert c.resources
  assert 9 == len(c.resources), c.resources
  assert 4 == len([x for x in c.resources if isinstance(x, camera.ElphelCamera)])
  assert 1 == len([x for x in c.resources
                   if isinstance(x, stepper.ImsStepperWrapper)])
  lights = [x for x in c.resources
            if isinstance(x, lighting.LightingController)]
  assert 1 == len(lights)
  assert [2, 3] == lights[0].GetTopLights()
  assert [1, 2, 3, 4] == lights[0].GetFrontLights()


class FooResource(object):

  def __init__(self, name):
    self.name = name


def testConfig():
  c = scanner_config.ScannerConfig()
  assert [] == c.resources
  assert [] == c.scanners
  assert [] == c.storage
  assert None == c.GetResource("none")
  assert None == c.packer


def testConfig_GetResourceNone():
  names = ["x-%s" % i for i in xrange(10)]
  c = scanner_config.ScannerConfig()
  c.scanners = [FooResource(n) for n in names]
  # scanners aren't resources.
  assert c.GetResource("x-1") is None
  c.storage = [FooResource(n) for n in names]
  # storage aren't resources, either.
  assert c.GetResource("x-1") is None


def testConfig_GetResource():
  c = scanner_config.ScannerConfig()
  names = ["x-%s" % i for i in xrange(10)]
  c.resources = [FooResource(n) for n in names]
  assert "x-1" == c.GetResource("x-1").name
  assert names == c.GetResourceNames()


def testConfig_GetResourceMulti():
  c = scanner_config.ScannerConfig()
  c.resources = [FooResource("x") for x in xrange(10)]
  try:
    c.GetResource("x")
    assert False, "Should have raised"
  except errors.ConfigError:
    pass
