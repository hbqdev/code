# Copyright 2012 Google Inc. All Rights Reserved.

"""Resources for storing API credentials."""
__author__ = "kwc@google.com (Ken Conley)"

import datetime
import os

import httplib2
from oauth2client import client

from resources import errors
from resources import katamari


def Register(factory):
  factory.RegisterFromDict("ServiceAccount", ServiceAccount.FromDict)


class Credentials(katamari.KatamariResource):
  """Abstract base class for credentials."""
  pass

class ServiceAccount(Credentials):
  """Service account credentials."""

  def __init__(self):
    self.service_account_email = None
    self.service_account_name = None
    self.private_key_file = None
    # Cache credentials.
    self._credentials = None

  def __str__(self):
    result = self.service_account_email
    if self._credentials is not None:
      result += "Token expires: " + self._credentials.token_expiry
      if self.IsExpired():
        result += " (expired)"
    return result

  @staticmethod
  def FromDict(raw_config):
    c = ServiceAccount()
    c.service_account_email = raw_config["service_account_email"]
    c.service_account_name = raw_config["service_account_name"]
    c.private_key_file = raw_config["private_key_file"]
    katamari.FromDict(c, raw_config)
    return c

  def IsExpired(self):
    expiry = self._credentials.token_expiry
    return (not expiry or
        datetime.datetime.utcnow() + datetime.timedelta(seconds=300) > expiry)

  def GetAuthToken(self, scope):
    """Get the auth token provided by these credentials.

    This method may take awhile as it blocks on an external authorization
    HTTP request.

    Args:
      scope: Scope to use for retrieiving auth token.
    Raises:
      errors.ConfigError: If credentials not configured correctly.
    """
    if not self.service_account_email:
      raise errors.ConfigError("Credentials not initialized")
    if not os.path.isfile(self.private_key_file):
      raise errors.ConfigError("private key file not available")

    if self._credentials is None:
      with open(self.private_key_file, 'r') as f:
        private_key = f.read()
      self._credentials = client.SignedJwtAssertionCredentials(
          self.service_account_email, private_key, scope)

    if self.IsExpired():
       self._credentials.refresh(httplib2.Http())
    return self._credentials.access_token
