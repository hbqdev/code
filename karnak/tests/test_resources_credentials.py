# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for resources.credentials."""
__author__ = "kwc@google.com (Ken Conley)"

import resources
from resources import credential
from resources import errors


def test_ServiceAccount():
  s = credential.ServiceAccount()
  assert s.service_account_email is None
  assert s.service_account_name is None
  assert s.private_key_file is None
  try:
    scope = 'https://www.googleapis.com/auth/devstorage.read'
    s.GetAuthToken(scope)
    assert False, "should have failed"
  except errors.Error:
    pass


def test_ServiceAccount_FromDict():
  d = dict(service_account_email="service@fake.com",
           service_account_name="service.fake.com",
           name="account 1",
           private_key_file="foo")
  s = credential.ServiceAccount.FromDict(d)
  assert "account 1" == s.name
  assert d == s.raw_config
  assert "service@fake.com" == s.service_account_email
  assert "service.fake.com" == s.service_account_name


def test_ServiceAccount_Factory_FromDict():
  d = dict(service_account_email="service@fake.com",
           service_account_name="service.fake.com",
           name="account 1",
           type="ServiceAccount",
           private_key_file="foo")
  factory = resources.DefaultFactory()
  s = factory.CreateFromDict(d)
  assert isinstance(s, credential.ServiceAccount)
  assert "account 1" == s.name
  assert d == s.raw_config
  assert "service@fake.com" == s.service_account_email
  assert "service.fake.com" == s.service_account_name


def test_ServiceAccount_FromDictFail():
  d = dict(private_key_file="foo")
  try:
    credential.ServiceAccount.FromDict(d)
    assert False, "Should have raised"
  except KeyError:
    pass


# TODO(kwc): delete this test once we no longer have credentials checked in.
def test_ServiceAccount_GetAuthToken():
  prefix = '682015002700-5gmoofr8s80voejnr8ld9h2nns2gvfcn'
  email = '%s@developer.gserviceaccount.com' % prefix
  name = '%s.apps.googleusercontent.com' % prefix
  private_key_file = ('keys/0d972c7184df27f390eb32ce3b3e68ec4ce5d9b9'
                      '-privatekey.p12')
  d = dict(service_account_email=email,
           service_account_name=name,
           name="account 1",
           private_key_file=private_key_file)
  c = credential.ServiceAccount.FromDict(d)
  scope = 'https://www.googleapis.com/auth/devstorage.read_write'
  try:
    val = c.GetAuthToken(scope)
    assert val, val
  except AttributeError as e:
    if 'sign' in str(e):
      # The oauth2client needs PyOpenSSL 0.11+, which is not installed on Lucid.
      pass
    else:
      raise
