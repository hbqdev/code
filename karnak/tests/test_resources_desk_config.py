# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests resources.desk_config."""
__author__ = "kwc@google.com (Ken Conley)"

import os

import resources
from resources import desk_config
from resources import errors
from tests import mock_hardware

TEST_FILE = "test_resources_desk_config.yaml"

mock_hardware.MockAll()


def GetResourcePath():
  return os.path.dirname(__file__)


def testLoadConfigFromFile_NoFile():
  factory = resources.DefaultFactory()
  try:
    desk_config.LoadConfigFromFile('not a file', factory)
    assert False, "Should have raised"
  except errors.ConfigError:
    pass


def testLoadConfigFromFile():
  factory = resources.DefaultFactory()
  test_file = os.path.join(GetResourcePath(), TEST_FILE)
  c = desk_config.LoadConfigFromFile(test_file, factory)
  assert c is not None
  assert c.desk is not None
  assert c.desk.IsInitialized()

  assert c.resources
  assert 3 == len(c.resources), c.resources
  desk = c.desk
  assert desk.GetScale() is not None
  assert desk.GetPrinter() is not None
  assert desk.GetPrinter()._handle == "/fake-dev/lphandle"
  assert desk.GetCheckinCamera() is not None


# Tripwire to make sure fake desk is working.
def testLoadConfigFromFile_FakeDesk():
  factory = resources.DefaultFactory()
  test_file = os.path.join("config", "fake_checkin_desk.yaml")
  c = desk_config.LoadConfigFromFile(test_file, factory)
  assert c is not None

  desk = c.desk
  assert desk is not None
  assert desk.IsInitialized()
  assert desk.GetScale() is not None
  assert desk.GetPrinter() is not None
  assert desk.GetCheckinCamera() is not None

