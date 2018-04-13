#!/usr/bin/python
"""Provides web interace to extract and view images archived in tar files.

Since TVCs by default do not have access to BigStore, this CGI script
allows a workaround for TVCs to view archived images on a backup server.

Debug and warning messages are stored in the /tmp/ in the format:
  librarian.persephone.www-data.<date>
"""
__author__ = ("willmartin@google.com (William Martin)")
__author__ = ("nguyenmic@google.com (Michael Nguyen)")

import cgi
import logging
import os
import re
import shutil
import tarfile

import kflags
import utils

# The backup location of the tarballs
BACKUP_PATH = "/scan/"
# The tarballs are downloaded from this directory
DOWNLOAD_PATH = "/tmp/www/"
# The tarballs are unpacked at this directory
UNPACKED_PATH = "/tmp/www/unpacked/"
# Hostname of the server hosting the backups
HOSTNAME = os.environ["SERVER_NAME"]

FLAGS = kflags.FLAGS
kflags.SetDefaults("logging", also_log_to_file=True,
                   daily_log=True, log_dir="/var/log/karnak/")


def IsPathValid(full_path):
  """Check if requested path is valid.

  Args:
    full_path: The path to the requested file or dir

  Returns:
    True, if path is valid otherwise False
  """
  if not os.path.exists(full_path):
    logging.warning("Requested path %s is not valid.", full_path)
    print"<b>It appears you tried to access an invalid path.<br>"
    print "Please click on the <a href=\"?\">HOME</a> link</b"

    return False

  return True


def CreateDownloadURL(tarfile_path):
  """Creates a HTTP link that auto-refreshes to download the tarball.

  Args:
    tarfile_path: The path to the tarball download.
  """
  tarball_file = os.path.basename(tarfile_path)
  shutil.copyfile(tarfile_path, DOWNLOAD_PATH + tarball_file)
  html_string = "<meta http-equiv=\"REFRESH\""
  html_string += "content=\"0;url=http://%s/tmp/%s\">" % (HOSTNAME,
                                                          tarball_file)
  print html_string

  logging.debug("%s tarball has been downloaded.", tarball_file)


def PrintUnpackedTarball(tarfile_path):
  """Display the contents of the unpacked tarball file.

  Args:
    tarfile_path: The path to the tarfile.
  """
  tarball_file = os.path.splitext(os.path.basename(tarfile_path))[0]
  tarball = tarfile.open(tarfile_path)
  tarball.extractall(path=UNPACKED_PATH)
  html_string = "<meta http-equiv=\"REFRESH\""
  html_string += "content=\"0;url=http://%s/tmp/unpacked/%s\">" % (HOSTNAME,
                                                                   tarball_file)
  print html_string

  logging.debug("%s tarball has been unpacked.", tarball_file)


def PrintRecentlyUnpacked(unpacked_dir):
  """Print out the recently unpacked tarballs at UNPACKED_PATH.

  Args:
    unpacked_dir: The directory location of the unpacked tarballs
  """
  unpacked_files = os.listdir(unpacked_dir)
  unpacked_files.sort()

  print "<div style=\";width:400px;float:left;\">"
  print "<h3>Recently Unpacked</h3>"

  for unpacked_file in unpacked_files:
    if os.path.isdir(unpacked_dir + unpacked_file):
      print "<a href=\"http://%s/tmp/unpacked/%s\">" % (HOSTNAME,
                                                        unpacked_file)
      print unpacked_file
      print "</a><br>"

  print "</div>"


def PrintDirectoryContents(backup_path, dir_path):
  """Print out the contents of a directory.

  Args:
    backup_path: The backup path of the tarballs
    dir_path: The directory path
  """
  print "<div style=\";width:550px;float:left\">"

  full_path = backup_path + dir_path
  if not IsPathValid(full_path):
    return

  directory_contents = os.listdir(full_path)
  directory_contents.sort()

  print "<h3>Index of %s</h3>" % dir_path
  if dir_path:
    one_dir_up = os.path.normpath(dir_path + "../")
    print "<a href=\"?path=%s/\">Go Back</a><br>" % (one_dir_up)

  for content in directory_contents:
    if re.search(r"\.tar$", content):
      print "%s: <a href=\"?path=%s%s\">Download</a>" % (content, dir_path,
                                                         content)
      print "<a href=\"?unpack=%s%s\">Unpack</a><br>" % (full_path, content)
    elif os.path.isdir(full_path + content):
      print "<a href=\"?path=%s%s/\">%s</a>" % (dir_path, content, content)
      print "[%d Items]<br>" % (len(os.listdir(full_path+content)))

  print "</div>"


def CGIFormCheck(cgi_form, backup_path):
  """Checks the cgi_form for HTTP variables.

  Args:
    cgi_form: The cgi form generated by cgi.FieldStorage()
    backup_path: The path to the backed up tarballs
  """
  accessed_url = "http://%s%s" % (HOSTNAME, backup_path)

  if "unpack" in cgi_form:
    tarball_path = cgi_form.getfirst("unpack")
    accessed_url += tarball_path
    logging.debug("%s URL has been accessed", accessed_url)

    if not IsPathValid(tarball_path):
      return
    PrintUnpackedTarball(tarball_path)

  elif "path" in cgi_form:
    path = cgi_form.getfirst("path")
    accessed_url += path
    logging.debug("%s URL has been accessed", accessed_url)

    if path == "./":
      PrintDirectoryContents(backup_path, "")
    elif re.search(r"\.tar$", path):
      CreateDownloadURL(backup_path + path)
      one_dir_up, _ = os.path.split(path)
      PrintDirectoryContents(backup_path, one_dir_up + "/")
    else:
      PrintDirectoryContents(backup_path, path)
  else:
    PrintDirectoryContents(backup_path, "")


def main():
  """Generate a CGI form for handling the web interace."""
  FLAGS.Parse()
  utils.InitializeLogging()

  cgi_form = cgi.FieldStorage()

  print "Content-type: text/html\n"
  print "<html>"
  print "<head><title>The Librarian</title></head>"
  print "<body>"
  print "<h2>Welcome to the Librarian</h2>"

  PrintRecentlyUnpacked(UNPACKED_PATH)
  CGIFormCheck(cgi_form, BACKUP_PATH)

  print "</body></html>"


if __name__ == "__main__":
  main()
