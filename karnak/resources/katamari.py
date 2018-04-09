# Copyright 2012 Google Inc. All Rights Reserved.

"""Base KatamariResource class used to model configuration objects."""
__author__ = "kwc@google.com (Ken Conley)"

import json
import os

import yaml

import resources
from resources import errors


def FromDict(resource, raw_config):
  """Loads common resources properties from dict config.

  Args:
    resource: KatamariResource to load into.
    raw_config: Configuration dict.
  """
  resource.name = raw_config["name"]
  resource.raw_config = raw_config


def LoadSectionList(raw_section_val, section_list, factory):
  if not type(raw_section_val) == list:
    raise errors.ConfigError("'%s' must be a list" % raw_section_val)
  del section_list[:]
  for config_value in raw_section_val:
    if not "type" in config_value:
      raise errors.ConfigError("Resource is missing required 'type' key: %s"
                               % str(config_value))
    resource = factory.CreateFromDict(config_value)
    if resource is None:
      raise errors.ConfigError("Failed to load [%s] resource: %s" %
                               (config_value["type"], config_value))
    section_list.append(resource)


class Config(object):
  """Configuration data."""

  __slots__ = ["raw_config", "resources", "base_directory", "scratch_directory"]

  def __init__(self):
    self.raw_config = None
    self.resources = []
    self.base_directory = "static"
    # NOTE: scratch dir is open to the outside.
    self.scratch_directory = os.path.join(self.base_directory, "tmp")

  @staticmethod
  def FromDict(raw_config, factory):
    """Creates new instances from dictionary.

    Args:
      raw_config: Configuration in dict representation.
      factory: ResourceFactory instance.
    Raises:
      errors.ConfigError: If configuration is invalid.
    """
    c = Config()
    c.raw_config = raw_config
    c.base_directory = raw_config["base_directory"]
    c.scratch_directory = raw_config["scratch_directory"]

    sections = ["resources"]
    for section in sections:
      section_list = getattr(c, section)
      LoadSectionList(raw_config.get(section, []), section_list, factory)
    # Two-phase load.
    for section in sections:
      section_list = getattr(c, section)
      for resource in section_list:
        resource.Init(c)
    return c

  def GetActions(self):
    return {}

  def GetResource(self, name):
    """Gets names of resources in this config.

    This will only fetch entities in the *resource* section of the
    configuration. Storage and Packer are not resources as they are
    declared in separate sections.

    Args:
      name: Resource name.
    Returns:
      Matching resource or None if no matching resource.
    Raises:
      errors.ConfigError: If multiple matching resources.
    """
    matches = [x for x in self.resources if x.name == name]
    if len(matches) == 1:
      return matches[0]
    elif len(matches) > 1:
      raise errors.ConfigError("Multiple resources with the name [%s]" % name)
    else:
      return None

  def GetResourceNames(self):
    """Gets names of resources in this config.

    Returns:
      List of resource name.
    """
    return [x.name for x in self.resources]

  def __str__(self):
    return "config: %s" % (yaml.dump(self.raw_config,
                                     default_flow_style=False))


def LoadConfigFromString(str_val, config_class=None, factory=None):
  """Loads and validation configuration from string.

  Args:
    str_val: Serialized config as YAML string.
    config_class: Config class to instantiate.  Defaults to katamari.Config.
    factory: Optional ResourceFactory instance.  Defaults to
        resources.DefaultFactory().
  Returns:
    Config instance.
  Raises:
    Error: If config fails to load or does not validate.
  """
  if factory is None:
    factory = resources.DefaultFactory()
  if config_class is None:
    config_class = Config
  config_dict = yaml.load(str_val)
  if not type(config_dict) == dict:
    raise errors.ConfigError("Config must be a YAML dictionary")
  return config_class.FromDict(config_dict, factory)


def LoadConfigFromFile(filename, config_class, factory=None):
  """Loads and validation configuration from file.

  Args:
    filename: Path to YAML-formatted file.
    config_class: Config class to instantiate.
    factory: Optional ResourceFactory instance.  Defaults to
        resources.DefaultFactory().
  Returns:
    Config instance.
  Raises:
    errors.ConfigError: If config fails to load or does not validate.
  """
  if not os.path.exists(filename):
    raise errors.ConfigError("Config file [%s] does not exist" % filename)
  with open(filename) as f:
    return LoadConfigFromString(f.read(), config_class, factory=factory)


class KatamariResource(object):
  """Default Katamari Resource definition, all node resources should extend this class."""

  __slots__ = ["name", "raw_config", "status"]

  def __init__(self):
    # Name and raw_config are public attributes.
    self.name = None
    self.raw_config = None
    self.status = None


  def Init(self, config):
    """Initializes resource with load config.

    This is the second pass of the resource configuration
    API.  Resources are instantiated and then Init() is called
    in a second pass.

    Args:
      config: Loaded Config instance.
    """
    pass

  def GetActions(self):
    return {}

  def GetName(self):
    return self.name

  def GetStatus(self):
    """Gets the status dict object for a resource.

    The Status is a dict of {key, value} pairs which may differ
    by resource type.  The status dict represents the current
    state and status of a given resource.
    """
    return self.status

  def UpdateStatus(self, status):
    """Updates the status object on a resource.

    See dict.update()

    Args:
      status: Dict object
    """
    self.status.update(status)

  def SetStatus(self, status):
    """Sets the entire status object on a resource.

    Args:
      status: Dict object
    """
    self.status = status

  def __str__(self):
    if self.raw_config:
      return "config: " + json.dumps(self.raw_config)
    else:
      return self.name or self.__class__.__name__
