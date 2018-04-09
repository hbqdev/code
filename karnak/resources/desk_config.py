# Copyright 2012 Google Inc. All Rights Reserved.

"""Processes check desk configuration."""
__author__ = "kwc@google.com (Ken Conley)"

import os

from resources import katamari


class DeskConfig(katamari.Config):
  """Configuration of checkin desk."""

  __slots__ = ["desk", "storage", "credentials"]

  def __init__(self):
    super(DeskConfig, self).__init__()
    self.desk = None
    self.credentials = []
    self.storage = []

  @staticmethod
  def FromDict(raw_config, factory):
    """Creates new instances from dictionary.

    Args:
      raw_config: Configuration in dict representation.
      factory: Config factory.
    Raises:
      errors.ConfigError: If configuration is invalid.
    """
    c = DeskConfig()
    c.raw_config = raw_config
    c.base_directory = raw_config["base_directory"]
    c.scratch_directory = os.path.join(c.base_directory,
                                       raw_config["scratch_directory"])

    c.desk = factory.CreateFromDict(raw_config["checkin"])
    sections = ["resources", "storage", "credentials"]
    for section in sections:
      section_list = getattr(c, section)
      katamari.LoadSectionList(
          raw_config.get(section, []), section_list, factory)
    # Two-phase load.
    for section in sections:
      section_list = getattr(c, section)
      for resource in section_list:
        resource.Init(c)
    c.desk.Init(c)
    return c


def LoadConfigFromFile(filename, factory=None):
  """Loads and validation checkin desk configuration from file.

  Args:
    filename: Name of file to load.
    factory: Optional ResourceFactory instance.  Defaults to
        resources.DefaultFactory().
  Returns:
    Config instance.
  Raises:
    Error: If config fails to load or does not validate.
  """
  return katamari.LoadConfigFromFile(filename, DeskConfig, factory=factory)
