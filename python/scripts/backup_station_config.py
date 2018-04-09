#!/usr/bin/python

"""Script to backup YAML configurations from scan stations.

NOTE: suggested to run from scanning-ops/scripts
 directory in your git client! Otherwise, look at help for
 path options.

Josh Weaver <jweaver@google.com>
"""

import logging
import os
import subprocess
import sys

import kflags
import stations
import utils

SRC_ROOT = "~/scanning-ops/karnak/config"
# defaults to being run from scanning-ops/scripts
DEST_ROOT = "../karnak/config"

FLAGS = kflags.FLAGS

kflags.AddArgument("--output_path", type=str,
                   default=DEST_ROOT,
                   action=stations.ExpandPaths,
                   help="output path for config files")

kflags.AddArgument("--create_path",
                   action="store_true",
                   default=False,
                   help="flag to create output_path if does not exist")


def EnsureDirExistsOrDie(output_path, create_if_missing=False):
  """Verify output_path exists or create if requested."""
  if not os.path.isdir(output_path):
    if create_if_missing:
      logging.debug("Creating directory %s", output_path)
      os.makedirs(output_path)
    else:
      logging.error("Not creating missing directory %s", output_path)
      sys.exit(1)


def main():
  """Backup station config files."""
  FLAGS.Parse()
  utils.InitializeLogging()
  exit_code = os.EX_OK

  scanstations = stations.Stations()

  EnsureDirExistsOrDie(FLAGS.output_path, FLAGS.create_path)

  for station, ip in scanstations.GetStationIPs().items():
    src_path = os.path.join(SRC_ROOT, station + ".yaml")
    dest_path = os.path.join(FLAGS.output_path, station + ".yaml")

    try:
      utils.CopyFilesFromRemoteServer(src_path, dest_path, ip)
    except subprocess.CalledProcessError as rsync_error:
      logging.error("Unable to backup file to %s", ip)
      logging.error(rsync_error)
      exit_code = os.EX_TEMPFAIL

  sys.exit(exit_code)


if __name__ == "__main__":
  main()
