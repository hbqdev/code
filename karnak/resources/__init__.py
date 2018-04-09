# Copyright 2012 Google Inc. All Rights Reserved.

"""Scan station resources."""
__author__ = "kwc@google.com (Ken Conley)"

import resources.camera
import resources.credential
import resources.desk
import resources.errors
import resources.lighting
import resources.packer
import resources.printer
import resources.scale
import resources.scanner
import resources.stepper
import resources.storage
import resources.crosshair
import resources.shoe_light


class ResourceFactory(object):
  """Creates new resource instances from config data."""

  def __init__(self):
    self._handlers = {}

  def RegisterFromDict(self, type_name, handler):
    """Registers handler for loading from config dictionary.

    Args:
      type_name: Resource type to register for.
      handler: Function to call with dict instance.
    """
    self._handlers[type_name] = handler

  def CreateFromDict(self, value, type_name=None):
    """Creates new resource from dictionary data.

    Args:
      value: Dictionary config data.
      type_name: Override resource type.
    Returns:
      Resource instance.
    """
    if type_name is None:
      type_name = value["type"]
    try:
      if type_name not in self._handlers:
        raise resources.errors.ConfigError(

            "No handler for type '%s'" % type_name)
      return self._handlers[type_name](value)
    except KeyError as e:
      raise resources.errors.ConfigError(
          "[%s]: Missing required %s key in:\n%s" %
          (type_name, str(e), value))



def DefaultFactory():
  """Creates ResourceFactory with default handlers.

  Returns:
    ResourceFactory instance.
  """
  factory = ResourceFactory()
  resources.camera.Register(factory)
  resources.credential.Register(factory)
  resources.desk.Register(factory)
  resources.lighting.Register(factory)
  resources.crosshair.Register(factory)
  resources.packer.Register(factory)
  resources.printer.Register(factory)
  resources.scale.Register(factory)
  resources.scanner.Register(factory)
  resources.stepper.Register(factory)
  resources.storage.Register(factory)
  resources.shoe_light.Register(factory)
  return factory
