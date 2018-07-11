"""Deletes old scan directories.

It works in X steps:

1) Look how much free space is left. If < BUFFER, remove dir(s).
2) Remove scan dirs starting from oldest date(s) until space has cleared.
3) Send an email about the deleted dir(s) and their size.

NOTE: To run on a 3D server, specify the --server_3d flag.
"""
import collections
import datetime
import glob
import logging
import os
import shutil
import sys

import kflags
import utils

# Relative path of the scans directories
SCANS_PATH = "/scan/"

FLAGS = kflags.FLAGS

kflags.AddArgument("--server_3d", action="store_true",
                   help="If True, script is being run on a 3D server")
kflags.AddArgument("--buffer_size", type=int, default=576716800,
                   help="Buffer size in GBs converted to KBs")
kflags.AddArgument("--glob_pattern", type=str, default="/scan/sbs*-backup",
                   help="Glob pattern to match scan directories")
kflags.AddArgument("--dry_run", action="store_true",
                   help="Test run. No dir(s) are deleted.")


def AvailableSpace(path):
  """Returns the free disk space at path.

  Args:
    path: The path to look at.

  Returns:
    The free disk space in KBs.
  """
  stats = os.statvfs(path)

  return (stats.f_bavail*stats.f_frsize)/1024


def GetDeletedDirectoryString(deleted_dirs):
  """Iterate over list to generate html string from deleted_dirs.

  Args:
    deleted_dirs: Dictionary of deleted dir(s) path and size

  Returns:
    HTML string
  """
  string = "Deleted Directories:<br>\n"

  for path, size in deleted_dirs:
    new_size = utils.ConvertSize(size)
    string += "Deleted <b>%s</b> Size <b>%s</b><br>\n" % (path, new_size)

  return string


def SendCleanUpEmail(deleted_dirs, free_space, new_free_space):
  """Sends out an email detailing what was deleted.

  Args:
    deleted_dirs: Dictionary of deleted directories
    free_space: Converted string of the free space before delete
    new_free_space: Converted string of the free space after delete
  """
  before_string = "Before cleanup: %s free<br><br>" % free_space
  deleted_string = GetDeletedDirectoryString(deleted_dirs) + "<br>"
  after_string = "After cleanup: %s free" % new_free_space

  now = datetime.datetime.now().strftime("%A %b %d %H:%M:%S PDT")
  email_subject = "Storage Alert for %s" % now
  email_message = before_string + deleted_string + after_string
  utils.SendEmailToTechs(email_subject, email_message)


def GetDirectories2d(glob_pattern):
  """Generates the dictionary of dirs and size to clean up on a backup server.

  Args:
    glob_pattern: Glob pattern string of the 2D backup directories

  Returns:
    backup_dirs: A dict mapping date to a list of 2-tuples(dir, size)
  """
  backup_dirs = collections.defaultdict(list)

  for station in glob.glob(glob_pattern):
    dates = os.listdir(station)

    for date in dates:
      backup_path = os.path.join(station, date)
      backup_size = sum([os.path.getsize(os.path.join(backup_path, p))/(1024)
                         for p in os.listdir(backup_path)])
      backup_dirs[date].append((backup_path, backup_size))

  return backup_dirs


def GetDirectories3d(glob_pattern):
  """Generates the dictionary of dirs and size to clean up on a server_3d.

  Args:
    glob_pattern: Glob pattern of the 3D scan directories

  Returns:
    dirs_3d:  A dict mapping date to a list of 2-tuples(dir, size)
  """
  dirs_3d = collections.defaultdict(list)

  for scan_dir in glob.glob(glob_pattern):
    # Strip out the date from the 3d scan name
    date = os.path.basename(scan_dir).split("-")[0]

    size = sum([os.path.getsize(os.path.join(scan_dir, p))/(1024)
                for p in os.listdir(scan_dir)])
    dirs_3d[date].append((scan_dir, size))

  return dirs_3d


def CleanUp(server_3d, free_space, buffer_size, dry_run, glob_pattern):
  """Deletes the older directories until buffer is restored.

  Args:
    server_3d: if True, cleanup is being done on a 3d server
    free_space: Storage space between buffer and current size of SCANS_PATH
    buffer_size: Size of the buffer in KBs
    dry_run: Indicates a test run
    glob_pattern: glob pattern of the directories to be deleted

  Returns:
    Dictionary of deleted directories path and size
  """
  deleted_size = 0
  deleted_dirs = []

  if not server_3d:
    dirs_to_delete = GetDirectories2d(glob_pattern)
  else:
    dirs_to_delete = GetDirectories3d(glob_pattern)

  dates = dirs_to_delete.keys()
  dates.sort()

  for date in dates:
    logging.debug("Deleting date %s:", date)

    for directory, size in dirs_to_delete[date]:
      new_size = utils.ConvertSize(size)
      logging.debug("Deleting directory %s Size: %s", directory, new_size)

      if not dry_run:
        shutil.rmtree(directory)

      # Only add to the deleted_dir dictionary if size > 0
      if size:
        deleted_dirs.append((directory, size))
        deleted_size += size

      if free_space + deleted_size > buffer_size:
        logging.debug("Buffer space has been freed up. Terminating cleanup.")
        return deleted_dirs


def main():
  """Iterate through scan stations directories to free up space."""
  FLAGS.Parse()
  utils.InitializeLogging()

  free_space = AvailableSpace(SCANS_PATH)
  if free_space > FLAGS.buffer_size:
    logging.info("More than %s available",
                 utils.ConvertSize(FLAGS.buffer_size))
    sys.exit(0)

  logging.info("Not enough space. Begin cleaning.")
  deleted_dirs = CleanUp(FLAGS.server_3d, free_space, FLAGS.buffer_size,
                         FLAGS.dry_run, FLAGS.glob_pattern)
  SendCleanUpEmail(deleted_dirs, utils.ConvertSize(free_space),
                   utils.ConvertSize(AvailableSpace(SCANS_PATH)))


if __name__ == "__main__":
  main()
