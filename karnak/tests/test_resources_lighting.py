# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for resources.lighting."""
__author__ = "kwc@google.com (Ken Conley)"

import drivers.dmx
import drivers.power
import resources
from resources import lighting
from tests import mock_hardware

import mock

mock_hardware.MockAll()

FAKE_HANDLE = "FakeHandle"


def test_LightingController():
  l = lighting.LightingController(FAKE_HANDLE, [1, 2], [2, 3])
  assert l.name is None
  assert l.raw_config is None
  assert l._controller
  assert l._power
  assert [1, 2] == l.GetFrontLights()
  assert [2, 3] == l.GetTopLights()
  assert l.GetActions()


def test_LightingController_FromDict():
  d = dict(name="lighting", handle=FAKE_HANDLE, front_lights=[1, 2],
           top_lights=[3, 4, 5])
  s = lighting.LightingController.FromDict(d)
  assert "lighting" == s.name
  assert d == s.raw_config
  assert [1, 2] == s.GetFrontLights()
  assert [3, 4, 5] == s.GetTopLights()


def test_LightingController_Factory_FromDict():
  d = dict(name="lighting", type="LightingController", handle=FAKE_HANDLE,
           front_lights=[1, 2], top_lights=[3, 4])
  factory = resources.DefaultFactory()
  s = factory.CreateFromDict(d)
  assert isinstance(s, lighting.LightingController)
  assert [1, 2] == s.GetFrontLights()
  assert [3, 4] == s.GetTopLights()


def test_LightingController_FromDictFail():
  d = dict(name="lighting", type="LightingController")
  try:
    lighting.LightingController.FromDict(d)
    assert False, "Should have raised"
  except KeyError:
    pass


def GetMockLighting(front, top):
  l = lighting.LightingController(FAKE_HANDLE, front, top)
  l._power = mock.MagicMock(drivers.power.ChauvetDmx4Led)
  l._controller = mock.MagicMock(drivers.dmx.master.EntecUsbPro)
  l.settle_on = 0
  l.settle_off = 0
  return l


def test_LightingController_AllOn():
  l = GetMockLighting([], [])
  l.AllOn()
  l._power.allOn.assert_called_with()


def test_LightingController_AllOff():
  l = GetMockLighting([1, 2], [2, 3])
  l.AllOff()
  l._power.allOff.assert_called_with()
  l._controller.send.assert_called_with()


def test_LightingController_BankOn():
  l = GetMockLighting([1, 2], [2, 3])
  l.BankOn(2)
  l._power.setBank.assert_called_with(2, True)
  l._controller.send.assert_called_with()


def test_LightingController_BankOff():
  l = GetMockLighting([1, 2], [2, 3])
  l.BankOff(1)
  l._power.setBank.assert_called_with(1, False)
  l._controller.send.assert_called_with()


def test_LightingController_SwitchToFront():
  top = [1, 2]
  front = [3, 4]
  l = GetMockLighting(front, top)
  l.SwitchToFrontLighting()
  for b in front:
    assert mock.call(b, True) in l._power.setBank.call_args_list
  for b in top:
    assert mock.call(b, False) in l._power.setBank.call_args_list
  l._controller.send.assert_called_with()


def test_LightingController_SwitchToTop():
  top = [1, 2]
  front = [3, 4]
  l = GetMockLighting(front, top)
  l.SwitchToTopLighting()
  for b in front:
    assert mock.call(b, False) in l._power.setBank.call_args_list
  for b in top:
    assert mock.call(b, True) in l._power.setBank.call_args_list
  l._controller.send.assert_called_with()
