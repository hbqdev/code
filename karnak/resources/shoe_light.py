# -*- coding: utf-8 -*-
# Copyright 2013 Google Inc. All Rights Reserved.

"""Rescource API for shoe light.  All shoelights turn on and off together.

in the .yaml file, shoe_lights specifies the last digit of the address of
shoe lights in an array. i.e. if the shoelight address is x5002, the
shoe_lights in the yaml should be set to [2].

in the .yaml file, shoe_light_port specifies the USB port of the xbee
controller, i.e. ttyUSB0.

"""

__author__ = "katydek@google.com (Katie Dektar)"

from resources import katamari
from drivers import shoe_light


def Register(factory):
  factory.RegisterFromDict("ShoeLightController",ShoeLightController.FromDict)


class ShoeLight(katamari.KatamariResource):
  """Abstract ShoeLight resource."""

  #TODO: figure out what's wrong with this
  def __init__(self, port):
    super(ShoeLight, self).__init__()
    self._active = False
    try:
      self._shoelight = shoe_light.ShoeLight(port)
      self._active = True
    except:
      "could not connect to shoelight controller"

class ShoeLightController(ShoeLight):

  def GetActions(self):
    return{"on": self.on,
           "off": self.off}


  # here shoelight is what is specified in the .yaml under 'shoe_lights'
  def __init__(self, shoelightids, port):
    ShoeLight.__init__(self, port)
    self._shoelightids = shoelightids
    self.off()
    print "the shoe lights have started!"


  def on(self):
    if self._active:
      for shoe_id in self._shoelightids:
        self._shoelight.on(shoe_id)


  def off(self):
    if self._active:
      for shoe_id in self._shoelightids:
        self._shoelight.off(shoe_id)


  # creates a ShoeLightController from a dictionary
  @staticmethod
  def FromDict(raw_config):
    slc = ShoeLightController(raw_config["shoe_lights"], raw_config["shoe_light_port"])
    katamari.FromDict(slc, raw_config)
    return slc
