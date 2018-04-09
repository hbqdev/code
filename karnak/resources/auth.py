"""Auth server."""

from resources import errors
from resources import katamari


def Register(factory):
  factory.RegisterFromDict("AuthServer", AuthServer.FromDict)


class AuthServer(katamari.KatamariResource):
  """Resource model for the auth server."""

  def __init__(self, resource_names):
    super(AuthServer, self).__init__()
    self._initialized = False
    self._resource_names = resource_names
    self.resources = []

  @staticmethod
  def FromDict(raw_config):
    server = AuthServer(raw_config["resources"])
    katamari.FromDict(server, raw_config)
    return server

  def IsInitialized(self):
    return self._initialized

  def Init(self, config):
    super(AuthServer, self).Init(config)

    self.resources = []
    for resource_name in self._resource_names:
      resource = config.GetResource(resource_name)
      if resource is None:
        raise errors.ConfigError("[AuthServer] No resource named [%s]. "
                                 "Resources are: %s" %
                                 (resource_name, config.GetResourceNames()))
      self.resources.append(resource)
    self._initialized = True
