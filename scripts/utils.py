"""Library of utilties for scanning-ops programs.

More details here
"""

__author__ = ("jweaver@google.com (Josh Weaver)")

import email.mime.text
import getpass
import logging
import math
import os
import smtplib
import socket
import subprocess
import sys
import time

import kflags

# TODO(nguyenmic): Use email lists instead of specifying individual emails
_EMAIL_LIST = ["wellerm@google.com", "jalarson@google.com",
               "barbarap@google.com", "samgordon@google.com",
               "msymmons@google.com", "dshoopman@google.com",
               "jimbruce@google.com", "jweaver@google.com",
               "tintran@google.com", "jimmychou@google.com",
               "nguyenmic@google.com", "katydek@google.com"]
_KATAMARI_TECH_LIST = ["tintran@google.com", "jimmychou@google.com",
                       "nguyenmic@google.com", "katydek@google.com"]

LOG_LEVELS_CHOICES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

FLAGS = kflags.FLAGS
kflags.DefineArgumentGroup("logging", None)
kflags.AddArgumentToGroup("logging", "--log_level", type=str, default="INFO",
                          choices=LOG_LEVELS_CHOICES,
                          help="Desired console log level")
kflags.AddArgumentToGroup("logging", "--log_dir", type=str, default="/tmp",
                          help="Directory to store log file")
kflags.AddArgumentToGroup("logging", "--also_log_to_file", action="store_true",
                          help="Also write log data to disk")
kflags.AddArgumentToGroup("logging", "--daily_log", action="store_true",
                          help="Use a single log file per day")

kflags.DefineArgumentGroup("access", None)
kflags.AddArgumentToGroup("access", "--username", type=str,
                          default="katamari",
                          help="username to access servers",)
kflags.AddArgumentToGroup("access", "--backup_server", type=str,
                          default="miranda",
                          help="backup server",)

kflags.DefineArgumentGroup("email", None)
kflags.AddArgumentToGroup("email", "--no_email", action="store_true",
                          help="Disable email output to katamari team.")


def WritetoFile(filename, string):
  """Create file and write buffered string into it.

  Args:
    filename: Name of file being written to
    string: String to write into file
  """
  new_file = open(filename, "w")
  new_file.write(string)
  new_file.close()


def ConvertSize(size):
  """Convert KBs into human readable format.

  Args:
    size: Size of file or dir in KBs

  Returns:
    String of new size value and unit name.
  """
  if not size:
    return "0 KB"

  unit_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
  unit = int(math.floor(math.log(size, 1024)))
  size_of_unit = math.pow(1024, unit)
  new_size = round(size/size_of_unit, 1)

  return "%.1f %s" % (new_size, unit_name[unit])


def ConstructLogFilename():
  """Returns filename for logfile.

  Returns:
    string of the format:
     FLAGS.log_dir/<PGM>.<hostname>.<username>.YYYY-MM-DD[-HH-MM-SS]
    If the --daily-log flag is set, the date is only YYYY-MM-DD
  """
  base_name = os.path.basename(sys.argv[0])
  pgm_name = os.path.splitext(base_name)[0]
  if FLAGS.daily_log:
    time_str = time.strftime("%Y-%m-%d")
  else:
    time_str = time.strftime("%Y-%m-%d-%H-%M-%S")

  filename = "%s.%s.%s.%s.log" % (
      pgm_name,
      socket.gethostname(),
      getpass.getuser(),
      time_str)

  return os.path.join(FLAGS.log_dir, filename)


def InitializeLogging():
  """Configure logging to console and optionally to disk."""
  logger = logging.getLogger("")
  logger.setLevel(logging.DEBUG)

  # All scripts log to console
  console = logging.StreamHandler()
  console.setLevel(FLAGS.log_level)
  formatter = logging.Formatter("%(levelname)-8s: %(message)s")
  console.setFormatter(formatter)
  logger.addHandler(console)

  logging.debug("Console logging started")

  if FLAGS.also_log_to_file:
    log_filename = ConstructLogFilename()
    disk = logging.FileHandler(filename=log_filename, mode="a")
    disk.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs).03d %(levelname)-8s %(message)s",
        "%Y-%m-%d %H:%M:%S")
    disk.setFormatter(formatter)
    logger.addHandler(disk)
    logging.debug("Also logging to %s", log_filename)

  logging.debug("Program %s has started", sys.argv[0])


def CopyFilesToRemoteServer(src_path, dest_path, keep_files=True,
                            user=None, server=None):
  """This runs rsync to copy files from a local machine to a remote server.

  Args:
    src_path: source path on local server
    dest_path: target path on remote server
    keep_files: if True, do not delete source files after successful copy
    user: username to access remote server
    server: hostname of remote server

  Returns:
    Subprocess output

  Raises:
    subprocess.CalledProcessError
  """
  if not user:
    user = FLAGS.username
  if not server:
    server = FLAGS.backup_server

  full_dest = "%s@%s:%s" % (user, server, dest_path)

  return CopyFiles(src_path, full_dest, keep_files)


def CopyFilesFromRemoteServer(src_path, dest_path, server,
                              keep_files=True, user=None):
  """This runs rsync to copy files from a remote server to the local machine.

  Args:
    src_path: source path on remote server
    dest_path: target path on local server
    server: hostname of remote server
    keep_files: if True, do not delete source files after successful copy
    user: username to access remote server

  Returns:
    Subprocess output

  Raises:
    subprocess.CalledProcessError
  """
  if not user:
    user = FLAGS.username

  full_src = "%s@%s:%s" % (user, server, src_path)

  return CopyFiles(full_src, dest_path, keep_files)


def CopyFiles(src_path, dest_path, keep_files=True):
  """Copy all files in src_path to dest_path.

  Args:
    src_path: source file location
    dest_path: source file destination
    keep_files: if True, do not delete source files after successful copy

  Returns:
    Subprocess output

  Raises:
    subprocess.CalledProcessError
  """
  if keep_files:
    command = ["/usr/bin/rsync", "-a", "--timeout=5", src_path, dest_path]
  else:
    command = ["/usr/bin/rsync", "-a", "--timeout=5", "--remove-source-files",
               src_path, dest_path]

  return CheckSubprocessCall(command)


def CheckSubprocessCall(cmd, cwd=None):
  """Subprocess.check_output() wrapper.

  Args:
    cmd: command formatted into a list
    cwd: if not None, the process' current directory will be
         changed to cwd before it is executed

  Returns:
    Subprocess output

  Raises:
    subprocess.CalledProcessError
  """
  logging.debug("Executing command %s", (" ").join(cmd))

  process_output = subprocess.check_output(cmd, cwd=cwd,
                                           stderr=subprocess.PIPE)

  if process_output:
    logging.debug(process_output)

  return process_output


def SendEmailToTechs(subject, message):
  """SendEmail() wrapper to send email only to katamari tech team.

  Args:
    subject: the subject line of the email
    message: the message for the email
  """
  SendEmail(subject, message, _KATAMARI_TECH_LIST)


def SendEmail(subject, message, recipients=_EMAIL_LIST):
  """Formats an email structure and sends out the email.

  Args:
    subject: the subject line of the email
    message: the message for the email
    recipients: email recipients
  """
  if FLAGS.no_email:
    logging.info("--no-email flag detected. Disabling email output.")
    return

  email_from = "Katamari"
  email_to = recipients

  # Create a plain text message
  msg = email.mime.text.MIMEText(message, "html")
  msg["Subject"] = subject
  msg["From"] = email_from
  msg["To"] = ", ".join(email_to)

  s = smtplib.SMTP("localhost")
  s.sendmail(email_from, email_to, msg.as_string())
  s.quit()


def main():
  # TODO(jweaver): give examples
  pass

if __name__ in "__main__":
  main()
