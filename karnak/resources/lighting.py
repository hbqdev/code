# Copyright 2012 Google Inc. All Rights Reserved.

import time

from resources import katamari

from drivers import power
from drivers import dmx

# Number of seconds to sleep after an 'on' operation to let lights settle to on.
SETTLING_TIME_ON = 3.5
SETTLING_TIME_OFF = 1.0

def Register(factory):
  factory.RegisterFromDict("LightingController", LightingController.FromDict)


class Lighting(katamari.KatamariResource):
  """Marker class for lighting hardware."""

  def __init__(self):
    katamari.KatamariResource.__init__(self)


class LightingController(Lighting):

  # Would be nice but getting NoneType errors, static call?
  def GetActions(self):
    return {"all on": self.AllOn,
            "all off": self.AllOff,
            "bank1on": self.Bank1On,
            "bank1off": self.Bank1Off,
            "bank2on": self.Bank2On,
            "bank2off": self.Bank2Off,
            "bank3on": self.Bank3On,
            "bank3off": self.Bank3Off,
            "bank4on": self.Bank4On,
            "bank4off": self.Bank4Off,
            "top": self.SwitchToTopLighting,
            "front": self.SwitchToFrontLighting,
            "preview": self.SwitchToPreviewLighting,
            "bottom": self.SwitchToBottomLighting}

  def __init__(self, handle, front_lights, top_lights, preview_lights, bottom_lights=None):
    Lighting.__init__(self)
    print "starting lighting with %s" % handle
    if "fake" not in handle:
      self._controller = dmx.master.EntecUsbPro(handle)
      self._power = power.ChauvetDmx4Led(1)
      # Add the power controller to the DMX chain in the controller
      self._controller.append(self._power)
    else:
      self._controller = None
    self._front_lights = front_lights
    self._top_lights = top_lights
    self._preview_lights = preview_lights
    self._bottom_lights = bottom_lights or []

    self.settle_on = SETTLING_TIME_ON
    self.settle_off = SETTLING_TIME_OFF

  @staticmethod
  def FromDict(raw_config):
    d = LightingController(raw_config["handle"], 
			   raw_config["front_lights"], 
			   raw_config["top_lights"],
                           raw_config["preview_lights"],
         raw_config.get("bottom_lights", []))
    katamari.FromDict(d, raw_config)
    return d

  def isMonotonous(self):
    return self._front_lights == self._top_lights

  def Bank1On(self):
    return self.BankOn(1)

  def Bank1Off(self):
    return self.BankOff(1)

  def Bank2On(self):
    return self.BankOn(2)

  def Bank2Off(self):
    return self.BankOff(2)

  def Bank3On(self):
    return self.BankOn(3)

  def Bank3Off(self):
    return self.BankOff(3)

  def Bank4On(self):
    return self.BankOn(4)

  def Bank4Off(self):
    return self.BankOff(4)

  def GetTopLights(self):
    return self._top_lights

  def GetFrontLights(self):
    return self._front_lights

  def AllOn(self):
    self._power.allOn()
    self._controller.send()
    time.sleep(self.settle_on)

  def BankOn(self, bank):
    self._power.setBank(bank, True)
    self._controller.send()
    time.sleep(self.settle_on)

  def BankOff(self, bank):
    self._power.setBank(bank, False)
    self._controller.send()
    time.sleep(self.settle_off)

  def AllOff(self):
    self._power.allOff()
    self._controller.send()
    time.sleep(self.settle_off)

  def SwitchTo(self, scene):
    for bank in (1, 2, 3, 4):
      lit = bank in scene
      self._power.setBank(bank, lit)
    self._controller.send()
    time.sleep(self.settle_on)

  def SwitchToFrontLighting(self):
    self.SwitchTo(self._front_lights)

  def SwitchToTopLighting(self):
    self.SwitchTo(self._top_lights)
  
  def SwitchToPreviewLighting(self):
    self.SwitchTo(self._preview_lights)

  def SwitchToBottomLighting(self):
    self.SwitchTo(self._bottom_lights)

