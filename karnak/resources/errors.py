# Copyright 2012 Google Inc. All Rights Reserved.

"""Error types."""
__author__ = "kwc@google.com (Ken Conley)"


class Error(Exception):
  """Error base class."""
  pass


class ConfigError(Error):
  """Error in system configuration."""
  pass


class InternalError(Error):
  """Unexpected internal error (bug)."""
  pass


class IOError(Error):
  """I/O error."""
  pass
