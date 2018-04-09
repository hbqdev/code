"""Processes auth server configuration."""

import os

from resources import katamari


class AuthConfig(katamari.Config):
  """Configuration of auth server."""

  __slots__ = ["storage", "credentials"]

  def __init__(self):
    super(AuthConfig, self).__init__()
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
    c = AuthConfig()
    c.raw_config = raw_config
    c.base_directory = raw_config["base_directory"]
    c.scratch_directory = os.path.join(c.base_directory,
                                       raw_config["scratch_directory"])

    sections = ["storage", "credentials"]
    for section in sections:
      section_list = getattr(c, section)
      katamari.LoadSectionList(
          raw_config.get(section, []), section_list, factory)
    # Two-phase load.
    for section in sections:
      section_list = getattr(c, section)
      for resource in section_list:
        resource.Init(c)
    return c


def LoadConfigFromFile(filename, factory=None):
  """Loads and validates checkin desk configuration from file.

  Args:
    filename: Name of file to load.
    factory: Optional ResourceFactory instance.  Defaults to
        resources.DefaultFactory().
  Returns:
    Config instance.
  Raises:
    Error: If config fails to load or does not validate.
  """
  return katamari.LoadConfigFromFile(filename, AuthConfig, factory=factory)
