# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for resources.storage."""
__author__ = "kwc@google.com (Ken Conley)"

import resources
from resources import errors
from resources import storage


def test_BigStore():
  s = storage.BigStore()
  assert s.name is None
  assert s.raw_config is None
  try:
    s.UploadFiles("K0000000000", ["fake-file"])
    assert False, "should have raised"
  except errors.InternalError:
    pass


def test_BigStore_FromDict():
  d = dict(name="storage", bucket="my bucket")
  s = storage.BigStore.FromDict(d)
  assert "storage" == s.name, s.name
  assert d == s.raw_config
  assert "my bucket" == s._bucket


def test_BigStore_Factory_FromDict():
  d = dict(name="storage", bucket="my bucket", type="BigStore")
  factory = resources.DefaultFactory()
  s = factory.CreateFromDict(d)
  assert isinstance(s, storage.BigStore)


def test_BigStore_FromDictFail():
  d = dict(name="storage")
  try:
    storage.BigStore.FromDict(d)
    assert False, "Should have raised"
  except KeyError:
    pass
