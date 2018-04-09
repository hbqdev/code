# Copyright 2012 Google Inc. All Rights Reserved.

"""Modified oauth2_plugin to add service accounts support.

To use, import and either:

1) Call ConfigurePlugin() prior to creating boto objects:

oauth2_service.ConfigurePlugin(service_account_email, private_key_file)

2) Add these settings to the OAuth2 section of the boto config file:
 * service_account_email
 * service_account_private_key_file
"""
__author__ = 'kwc@google.com (Ken Conley)'

import boto
import boto.auth_handler

import gslib
from gslib.cred_types import CredTypes
from gslib.third_party.oauth2_plugin import oauth2_client
from gslib.third_party.oauth2_plugin import oauth2_helper


SCOPE_BIGSTORE_READ_WRITE = 'https://www.googleapis.com/auth/devstorage.read_write'
SCOPE_BIGSTORE_FULL_CONTROL = 'https://www.googleapis.com/auth/devstorage.full_control'
SCOPE_XAPI = 'https://www.googleapis.com/auth/xapi'


def ConfigurePlugin(service_account_email, private_key_file):
  """Stores the plugin configuration inside the global boto config.

  Args:
    service_account_email: E-mail address of service account.
    private_key_file: File with private key data.
  """
  # This is a bit dirty to store in the global state, but boto's plugin
  # API does not appear to offer any other way to configure values into
  # a plugin.
  boto.config.set('Credentials', 'gs_service_client_id', service_account_email)
  boto.config.set('Credentials', 'gs_service_key_file', private_key_file)


# This follows the oauth2_plugin API.  Due to the way boto plugins work,
# it is important not to load the actual oauth2_plugin submodule.
class OAuth2AuthWithJwt(boto.auth_handler.AuthHandler):
  """boto AuthHandler plugin for OAuth2 with Signed JWT credentials."""

  capability = ['google-oauth2', 's3']

  def __init__(self, path, config, provider):
    if (provider.name == 'google'
        and config.has_option('Credentials', 'gs_service_client_id')
        and config.has_option('Credentials', 'gs_service_key_file')):
      self.oauth2_client = oauth2_helper.OAuth2ClientFromBotoConfig(config,
          cred_type=CredTypes.OAUTH2_SERVICE_ACCOUNT)

      # Initialize token cache and related locking
      gslib.util.InitializeMultiprocessingVariables()
      oauth2_client.InitializeMultiprocessingVariables()

    else:
      raise boto.auth_handler.NotReadyToAuthenticate()

  def add_auth(self, http_request):
    http_request.headers['Authorization'] = (
        self.oauth2_client.GetAuthorizationHeader())



