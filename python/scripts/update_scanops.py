#!/usr/bin/python

"""Update Scanning-Ops software on a scanstation from tarball source.

This script installs or upgrades the scanstation software from a
scanops tarball. It is run in the katamari root directory on a scanstation.

The install process has a few side effects:

1) The old software (~/scanning-ops) is moved to (~/scanning-ops-old).
 Older versions are deleted.

2) Log files are copied from the old software to the new software.

3) Some post install tasks are run, such as running Makefiles.

Typical usage is:
  update_scanops.py scanops-20140101.0.tgz

"""


import logging
import os
import shutil
import socket
import subprocess
import tarfile
import time

import kflags
import utils


FLAGS = kflags.FLAGS
kflags.AddArgument("tarfile", help="path to tarfile")

# Home directory
HOME = "/scan/katamari"
# Base name of software install
SOFTWARE_ROOT = os.path.join(HOME, "scanning-ops")
# Base name for previous software install
BACKUP_ROOT = os.path.join(HOME, "scanning-ops-old")
# Path of new karnak software
KARNAK_ROOT = os.path.join(SOFTWARE_ROOT, "karnak")
# Path of tarballs to archive
TARBALL_ROOT = os.path.join(KARNAK_ROOT, "static/tarballs/")
# Path of log files relative to software_root
LOG_PATH = "karnak/static/logs/"
# Scripts directory location
SCRIPTS_ROOT = os.path.join(SOFTWARE_ROOT, "scripts")


class Error(Exception):
  """Base error class."""
  pass


class FileError(Error):
  """File error."""
  pass


class MakeError(Error):
  """Make error."""
  pass


class ConfigError(Error):
  """Config error."""
  pass


def BackupTarballs(src_path):
  """Backup any existing tarballs.

  Args:
    src_path: location of tarball files to archive
  Returns:
    True if files successfully backed up
  """

  # Generate useful stats for user waiting for completion
  files = os.listdir(src_path)

  size = sum(os.path.getsize(os.path.join(src_path, f)) for f in files
             if os.path.isfile(os.path.join(src_path, f)))

  logging.info("Copying %d files (%s) from %s",
               len(files), utils.ConvertSize(size / 1024), src_path)

  dest_path = "/scan/%s-backup/%s/" % (
      socket.gethostname(),
      time.strftime("%Y-%m-%d"))

  try:
    utils.CopyFilesToRemoteServer(src_path, dest_path)
  except subprocess.CalledProcessError as rsync_error:
    logging.error("Unable to rsync files to backup server")
    logging.error(rsync_error)
    return False

  return True


def CopyLogs():
  """Copy logfiles from old software to new install.
  """
  src_path = os.path.join(BACKUP_ROOT, LOG_PATH)
  dst_path = os.path.join(SOFTWARE_ROOT, LOG_PATH)

  if not os.path.isdir(src_path):
    logging.info("No existing logs to copy")
    return

  files = os.listdir(src_path)
  if not files:
    logging.info("No existing logs to copy")
  else:
    logging.info("Copying log files from %s to %s",
                 src_path, dst_path)
    for f in files:
      logging.debug("copying %s", f)
      shutil.copy(os.path.join(src_path, f), dst_path)


def VerifyParameters(tarball_file):
  """Verify install parameters before starting update.

  Args:
    tarball_file: tar archive for new software

  Returns:
    True if all tests pass
  """
  if os.getcwd() != HOME:
    logging.error("Script needs to run in %s", HOME)
    return False

  if not os.path.exists(tarball_file):
    logging.error("cannot find %s", tarball_file)
    return False

  if not tarfile.is_tarfile(tarball_file):
    logging.error("Invalid tar archive: %s", tarball_file)
    return False

  return True


def DoPreInstallTasks():
  """Configure system for install.

  In preperation to software install, this:
   - Deletes any old backups of the software
   - Copies data files to backup server
   - Moves the current software to backup location

  Raises:
    FileError if tarball backup fails

  """
  if os.path.islink(BACKUP_ROOT):
    logging.warn("Old software is a symlink. Unlinking")
    os.unlink(BACKUP_ROOT)
  elif os.path.isdir(BACKUP_ROOT):
    logging.debug("removing directory %s", BACKUP_ROOT)
    shutil.rmtree(BACKUP_ROOT)
  else:
    logging.info("No backup directory at %s", BACKUP_ROOT)

  if os.path.isdir(TARBALL_ROOT) and os.listdir(TARBALL_ROOT):
    if not BackupTarballs(TARBALL_ROOT):
      raise FileError("Tarball backup failed, aborting install")
  else:
    logging.info("No tarballs to backup")

  if os.path.islink(SOFTWARE_ROOT):
    logging.debug("Moving software symlink to backup")
    old_target = os.readlink(SOFTWARE_ROOT)
    os.unlink(SOFTWARE_ROOT)
    os.symlink(old_target, BACKUP_ROOT)
  elif os.path.isdir(SOFTWARE_ROOT):
    logging.debug("Moving software directory to backup")
    shutil.move(SOFTWARE_ROOT, BACKUP_ROOT)
  else:
    logging.info("No source directory at %s", SOFTWARE_ROOT)


def InstallScanops(tarball_file):
  """Unpacks tarball_file to install Scanning-Ops software.

  Args:
    tarball_file: the tar archive

  Raises:
    FileError if tar cannot be unpacked

  """
  cmd = ["tar", "-xzf", tarball_file]

  try:
    utils.CheckSubprocessCall(cmd)
  except subprocess.CalledProcessError as tar_error:
    logging.error(tar_error)
    raise FileError("Unable to untar %s" % tarball_file)

  os.remove(tarball_file)


def DoPostInstallTasks():
  CopyLogs()
  cmd = ["make", "proto"]

  try:
    utils.CheckSubprocessCall(cmd, cwd=KARNAK_ROOT)
  except subprocess.CalledProcessError as make_error:
    logging.error(make_error)
    raise MakeError("make proto failed in %s directory" % KARNAK_ROOT)


def MakeStart():
  """Make an executable of start.py and move it to karnak.

  Raisers:
     MakeError if make start cannot run
  """

  cmd = ["make", "start"]
  try:
    utils.CheckSubprocessCall(cmd, cwd=SCRIPTS_ROOT)
  except subprocess.CalledProcessError as make_start_error:
    logging.error(make_start_error)
    raise MakeError("make start.py failed in %s directory" % SCRIPTS_ROOT)

  shutil.move(os.path.join(SCRIPTS_ROOT, "start"), KARNAK_ROOT)


def UpdateScanops():
  """Updates or installs Scanning-Ops software.

  Raises:
    ConfigError if parameters are incorrect
  """
  if not VerifyParameters(FLAGS.tarfile):
    raise ConfigError("Aborting install")

  DoPreInstallTasks()

  InstallScanops(FLAGS.tarfile)

  DoPostInstallTasks()

  MakeStart()

  logging.info("Update Finished.")


def main():
  FLAGS.Parse()

  utils.InitializeLogging()
  UpdateScanops()

if __name__ in "__main__":
  main()
