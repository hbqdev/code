# Copyright 2012 Google Inc. All Rights Reserved.

"""Processes scan station configuration."""
__author__ = "kwc@google.com (Ken Conley)"

import os

from resources import katamari
from resources import scanner
from resources import station


class ScannerConfig(katamari.Config):
  """Configuration of scan station."""

  __slots__ = ["station", "credentials", "scanners", "storage",
      "packer"]

  def __init__(self):
    super(ScannerConfig, self).__init__()
    self.station = None
    self.credentials = []
    self.scanners = []
    self.storage = []
    self.packer = None


  @staticmethod
  def FromDict(raw_config, factory):
    """Creates new instances from dictionary.

    Args:
      raw_config: Configuration in dict representation.
      factory: Config factory.
    Raises:
      errors.ConfigError: If configuration is invalid.
    """
    c = ScannerConfig()
    c.raw_config = raw_config

    c.base_directory = raw_config["base_directory"]
    c.scratch_directory = os.path.join(c.base_directory,
                                       raw_config["scratch_directory"])

    c.station = station.Station.FromDict(raw_config["station"])
    c.packer = factory.CreateFromDict(raw_config["packer"])
    sections = ["resources", "storage", "scanners", "credentials"]
    for section in sections:
      section_list = getattr(c, section)
      katamari.LoadSectionList(
          raw_config.get(section, []), section_list, factory)
    # Two-phase load.
    for section in sections:
      section_list = getattr(c, section)
      for resource in section_list:
        resource.Init(c)

    # Use extend for backwards compatibility.
    c.scanners.extend([s for s in c.resources
                       if isinstance(c, scanner.Scanner)])
    return c


def LoadConfigFromFile(filename, factory=None):
  """Loads and validation scan station configuration from file.

  Args:
    filename: Path to YAML-formatted file.
    factory: Optional ResourceFactory instance.  Defaults to
        resources.DefaultFactory().
  Returns:
    Config instance.
  Raises:
    Error: If config fails to load or does not validate.
  """
  return katamari.LoadConfigFromFile(filename, ScannerConfig, factory)
