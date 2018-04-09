# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests resources.packer."""
__author__ = "kwc@google.com (Ken Conley)"

import os
import tempfile

from resources import executors
from resources import packer
from resources import scanner
from resources import scanner_config
from resources import station


def test_Create():
  working_dir = tempfile.gettempdir()
  d = os.path.join(working_dir, "foo", "my_capture")
  output_dir = os.path.join(working_dir, "bar, ""my_output")
  config = scanner_config.ScannerConfig()
  config.station = station.Station()
  config.station.name = "my station"
  m = scanner.CreateManifest(config, "K5678")
  executor = executors.MockExecutor()

  p = packer.Tarball(output_dir)
  output_name = p.Create(d, m, working_dir=working_dir, executor=executor)

  # Verify the output filename.
  expected_output = "%s.tar" % (os.path.basename(d))
  expected_output = os.path.join(output_dir, expected_output)
  expected_output = os.path.abspath(expected_output)
  assert expected_output == output_name

  expected = "tar cf %s %s" % (expected_output, os.path.relpath(d, working_dir))
  assert expected == executor.last_command, executor.last_command
  assert working_dir == executor.last_kwds["cwd"]
