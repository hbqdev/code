# -*- coding: utf-8 -*-
# Copyright 2012 Google Inc. All Rights Reserved.

"""Resource API for printers."""

from resources import katamari

from drivers import controller

def Register(factory):
  factory.RegisterFromDict("Crosshair", Crosshair.FromDict)

class Crosshair(katamari.KatamariResource):
  """Abstract Printer resource."""

  def __init__(self, ip_address):
    super(Crosshair, self).__init__()
    self._active = False
    try:
      self._controller = controller.Controller(ip_address)
      self._active = True
    except :
      print "Could not contact the crosshair controller."

  def GetActions(self):
    return {"on": self.on, "off": self.off }
 
  def on(self):
    if self._active:
      self._controller.crosshairs(True)

  def off(self):
    if self._active:
      self._controller.crosshairs(False)


  @staticmethod
  def FromDict(raw_config):
    s = Crosshair(raw_config["address"])
    katamari.FromDict(s, raw_config)
    return s


