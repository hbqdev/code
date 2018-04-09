# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for resources.stepper."""
__author__ = "kwc@google.com (Ken Conley)"

import resources
from resources import stepper
from tests import mock_hardware

FAKE_ADDRESS = "192.168.255.255"
FAKE_PORT = -1

# Disable hardware.
mock_hardware.MockAll()


def test_ImsStepperWrapper():
  s = stepper.ImsStepperWrapper(100, FAKE_ADDRESS, FAKE_PORT)
  assert 100 == s._steps
  assert 0 == s._segments
  assert s.name is None
  assert s.raw_config is None
  assert s._stepper is not None


def test_ImsStepperWrapper_FromDict():
  d = dict(name="Stepper", port=1234, address=FAKE_ADDRESS, steps=5678)
  s = stepper.ImsStepperWrapper.FromDict(d)
  assert "Stepper" == s.name
  assert d == s.raw_config
  assert 5678 == s._steps
  assert s._stepper is not None


def test_ImsStepperWrapper_FactoryFromDict():
  d = dict(name="Stepper", port=1234, steps=5678, address=FAKE_ADDRESS, type="ImsStepper")
  factory = resources.DefaultFactory()
  s = factory.CreateFromDict(d)
  assert isinstance(s, stepper.ImsStepperWrapper)


def test_ImsStepperWrapper_FromDictFail():
  d = dict(port=1234, steps=5678)
  try:
    stepper.ImsStepperWrapper.FromDict(d)
    assert False, "Should have raised"
  except KeyError:
    pass


def test_FakeStepper():
  d = dict(name="fake")
  s = stepper.FakeStepper.FromDict(d)
  assert "fake" == s.name
  assert d == s.raw_config
  s.Step(123)
  s.StepOneSegment()


def test_FakeStepper_FactoryFromDict():
  d = dict(name="Stepper", type="FakeStepper")
  factory = resources.DefaultFactory()
  s = factory.CreateFromDict(d)
  assert isinstance(s, stepper.FakeStepper)
