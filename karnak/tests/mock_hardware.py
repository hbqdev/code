# Copyright 2012 Google Inc. All Rights Reserved.

"""Disable hardware drivers for software testing."""
__author__ = "kwc@google.com (Ken Conley)"

import mock

import drivers.controller
import drivers.dmx
import drivers.power
import drivers.stepper


def MockAll():
  # Disable hardware.
  drivers.controller.Controller = mock.MagicMock(drivers.controller.Controller)
  drivers.dmx.master.EntecUsbPro = mock.MagicMock(drivers.dmx.master.EntecUsbPro)
  drivers.power.ChauvetDmx4Led = mock.MagicMock(drivers.power.ChauvetDmx4Led)
  drivers.scale.Dymo = mock.MagicMock(drivers.scale.Dymo)
  drivers.stepper.ImsStepper = mock.MagicMock(drivers.stepper.ImsStepper)
