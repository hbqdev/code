#!/usr/bin/python

"""Copy one or more files to scan stations.

NOTE: unless you have ssh keys pushed to the scanstations,
you will be prompted for a password on each file transfer!

Josh Weaver <jweaver@google.com>
"""

import logging
import os
import subprocess

import kflags
import stations
import utils

FLAGS = kflags.FLAGS
kflags.SetDefaults("stations", type=["prod", "canary"])
kflags.AddArgument("files", type=str, nargs="+",
                   action=stations.ExpandPaths,
                   help="file(s) to copy to scanstations")
kflags.AddArgument("--dest", type=str,
                   default="~/",
                   action=stations.ExpandPaths,
                   help="target directory on scanstation")


class Error(Exception):
  """Base error class."""
  pass


class FileError(Error):
  """File Error."""
  pass


def CopyFileToServer(src_file, dest_ip, dest_path):
  """Copy the desired file from src_path to dest_path on dest_ip.

  Args:
    src_file: source file path
    dest_ip: IP of destination station
    dest_path: destination path for source file

  Raises:
    FileError if source file is not found
  """
  if not os.path.isfile(src_file):
    raise FileError("Unable to find file %s" % src_file)

  try:
    utils.CopyFilesToRemoteServer(src_file, dest_path, server=dest_ip)
  except subprocess.CalledProcessError as rsync_error:
    logging.error("Unable to deploy file to %s", dest_ip)
    logging.error(rsync_error)


def main():
  """Copy files to stations."""
  FLAGS.Parse()
  utils.InitializeLogging()

  scan_stations = stations.Stations()

  for station, ip in scan_stations.GetStationIPs().items():
    logging.info("Pushing to station %s", station)
    for src_file in FLAGS.files:
      CopyFileToServer(src_file, ip, FLAGS.dest)

if __name__ == "__main__":
  main()
