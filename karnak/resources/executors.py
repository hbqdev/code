# Copyright 2012 Google Inc. All Rights Reserved.

"""Command-line call executors."""
__author__ = "kwc@google.com (Ken Conley)"

import pexpect
import subprocess

from resources import errors


def PexpectExecutor(command):
  """Executes command via pexpect.

  Args:
    command: Command to execute.
  """
  capture = pexpect.spawn(command)
  capture.expect(pexpect.EOF)
  return capture.before

def CheckedSubprocessExecutor(command, **kwds):
  """Executes command via subprocess.check_call.

  Args:
    command: Command to execute.
  """
  try:
    kwds['shell'] = True
    subprocess.check_call(command, **kwds)
  except OSError as e:
    raise errors.InternalError("Command failed:\n%s\n%s" % 
                               (str(command), str(e)))


class MockExecutor(object):
  """Non-executor for testing."""

  def __init__(self):
    self.last_command = None
    self.last_kwds = None

  def __call__(self, command, **kwds):
    """Saves command to last_command for verification.

    Args:
      command: Command to (not) execute.
    """
    self.last_command = command
    self.last_kwds = kwds


def DefaultExecutor():
  return PexpectExecutor
