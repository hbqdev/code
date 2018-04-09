# Copyright 2012 Google Inc. All Rights Reserved.

"""Checkin desk."""
__author__ = "kwc@google.com (Ken Conley)"

from resources import camera
from resources import errors
from resources import katamari
from resources import printer
from resources import scale


def Register(factory):
  factory.RegisterFromDict("CheckinDesk", CheckinDesk.FromDict)


class CheckinDesk(katamari.KatamariResource):
  """Resource model for the checkin desk."""

  def __init__(self, resource_names):
    super(CheckinDesk, self).__init__()
    self._initialized = False

    self._resource_names = resource_names
    self._printer = None
    self._scale = None
    self._checkin_camera = None

  @staticmethod
  def FromDict(raw_config):
    scanner = CheckinDesk(raw_config["resources"])
    katamari.FromDict(scanner, raw_config)
    return scanner

  def IsInitialized(self):
    return self._initialized

  def Init(self, config):
    super(CheckinDesk, self).Init(config)

    self.resources = []
    for resource_name in self._resource_names:
      resource = config.GetResource(resource_name)
      if resource is None:
        raise errors.ConfigError("[CheckinDesk] No resource named [%s]. "
                                 "Resources are: %s" %
                                 (resource_name, config.GetResourceNames()))
      self.resources.append(resource)
      if isinstance(resource, printer.Printer):
        self._printer = resource
      if isinstance(resource, camera.Camera):
        self._checkin_camera = resource
      if isinstance(resource, scale.Scale):
        self._scale = resource
    if self._printer is None:
      raise errors.ConfigError("No printer in config")
    if self._scale is None:
      raise errors.ConfigError("No scale in config")
    if self._checkin_camera is None:
      raise errors.ConfigError("No checkin camera in config")
    self._initialized = True

  def GetPrinter(self):
    return self._printer

  def GetScale(self):
    return self._scale

  def GetCheckinCamera(self):
    return self._checkin_camera

