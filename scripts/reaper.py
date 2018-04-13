"""Transfers daily tarballs and log files to backup server.

Upon successful completion, old tarballs and capture files are removed.

Specify the --files-older-than to rsync files older than x minutes. Default
time is set to copy files older than 2 hours.

NOTE: This python script is run via crontab on the backup server.
"""
__author__ = ("nguyenmic@google.com (Michael Nguyen)")

import logging
import subprocess
import time

import kflags
import stations
import utils

# Directory location of backup file(s) on scan stations.
SRC_DIR = "/scan/katamari/scanning-ops/karnak/static"
# Directory location of where backup files are stored on the backup server.
DEST_DIR = "/scan"

FLAGS = kflags.FLAGS
kflags.SetDefaults("stations", type=["prod", "canary", "dev"])
kflags.AddArgument("--keep_files", action="store_true",
                   help="Keep old file(s) on scanstation after transfer")
kflags.AddArgument("--files_older_than", type=str, default="120",
                   help="Copy files older than x minutes.")


def DeleteCapture(station):
  """Delete the daily capture file(s).

  Args:
    station: hostname of the sbs server

  """
  files_location = "%s/capture/*" % SRC_DIR
  cmd = ["ssh", station, "rm", "-rf", files_location]

  try:
    utils.CheckSubprocessCall(cmd)
  except subprocess.CalledProcessError as delete_error:
    logging.error("Unable to delete raw images on %s", station)
    logging.error(delete_error)


def LogBackup(station, date):
  """Transfer log files to backup server.

  Args:
    station: hostname of the sbs server
    date: current date Y-m-d format

  """
  source = "%s/logs/log.txt" % (SRC_DIR)
  destination = "%s/%s-backup/%s/" % (DEST_DIR, station, date)

  try:
    utils.CopyFilesFromRemoteServer(source, destination, station)
  except subprocess.CalledProcessError as rsync_error:
    logging.error("Unable to rsync logs from %s", station)
    logging.error(rsync_error)


def CreateNewBackupDirectory(station, date):
  """Create the backup server directory if it doesn't already exist.

  Args:
    station: hostname of the sbs server
    date: current date Y-m-d format

  Returns:
    False if the backup directory cannot be created
  """
  new_backup_dir = "%s/%s-backup/%s" % (DEST_DIR, station, date)
  cmd = ["mkdir", "-p", new_backup_dir]

  try:
    utils.CheckSubprocessCall(cmd)
  except subprocess.CalledProcessError as mkdir_error:
    logging.error("Unable to create backup directory on %s", station)
    logging.error(mkdir_error)
    return False

  return True


def CheckTarballs(username, station, tarball_dir, files_older_than):
  """Check to see if the station has tarball files.

  Args:
    username: username to access station
    station: station IP address
    tarball_dir: directory where tarballs are stored
    files_older_than: time in minutes

  Returns:
    A list of tarballs older than copy_time
  """
  user_at_station = "%s@%s" % (username, station)
  cmd = ["ssh", user_at_station, "find", tarball_dir,
         "-mmin", "+" + files_older_than, "-type", "f"]
  try:
    tarballs = utils.CheckSubprocessCall(cmd)
  except subprocess.CalledProcessError as ssh_error:
    logging.error("Unable to retrieve list of tarballs from %s", station)
    logging.error(ssh_error)
    return []

  if not tarballs:
    logging.warning("No Tarballs found on %s", station)
    return []

  # Strip out the last newline character and return a list
  return [tarball for tarball in tarballs.rstrip("\n").split("\n")]


def TarballBackupandDelete(station, date, tarballs, keep_files):
  """Transfers tarball(s) to backup server and removes them after transfer.

  Args:
    station: hostname of the sbs server
    date: current date Y-m-d format
    tarballs: list of tarballs to rsync
    keep_files: if True, keep files on scanstation after transfer

  Returns:
    True if rsync is successful otherwise False
  """
  dest_dir = "%s/%s-backup/%s/" % (DEST_DIR, station, date)
  for tarball in tarballs:
    try:
      utils.CopyFilesFromRemoteServer(tarball, dest_dir, station, keep_files)
    except subprocess.CalledProcessError as rsync_error:
      logging.error("Unable to copy tarballs from %s", station)
      logging.error(rsync_error)
      return

  if keep_files:
    return

  DeleteCapture(station)


def main():
  """Iterate over array of SBS hostnames to backup SRC_DIR."""
  FLAGS.Parse()
  utils.InitializeLogging()

  scan_stations = stations.Stations()
  servers = scan_stations.GetStationIPs()

  date_today = time.strftime("%Y-%m-%d")

  for server in servers:
    logging.debug(server)
    # If the backup directory cannot be created, move onto the next station.
    if not CreateNewBackupDirectory(server, date_today):
      continue

    LogBackup(server, date_today)

    tarballs = CheckTarballs(FLAGS.username, server,
                             SRC_DIR + "/tarballs", FLAGS.files_older_than)
    # If station has no tarballs, then move on to the next station.
    if not tarballs:
      continue
    TarballBackupandDelete(server, date_today, tarballs, FLAGS.keep_files)


if __name__ == "__main__":
  main()
