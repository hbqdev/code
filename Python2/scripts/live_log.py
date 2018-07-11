#!/usr/bin/python
"""Simple cgi-wrapper script to simulate caching for the daily report script.

NOTE: Use the makefile to generate the live_log exe file.
"""
import datetime
import os

import generate_daily_report
import kflags
import utils

# Location of daily file
DAILY_FILE = "/tmp/dailysummaryemail.txt"
SECONDS = 60

FLAGS = kflags.FLAGS


def DumpFile(daily_file):
  """Opens the file and dumps the file content.

  Args:
    daily_file: daily file containing the scan data
  """
  with open(daily_file, "r") as daily_report:
    for line in daily_report:
      print line


def GetTimeDiff(daily_file):
  """Get the time difference between the daily file and current time.

  Args:
    daily_file: daily file containing the scan data

  Returns:
    time difference
  """
  file_timestamp = os.path.getmtime(daily_file)
  file_time = datetime.datetime.fromtimestamp(file_timestamp)

  now = datetime.datetime.now()
  return (now - file_time).total_seconds()/SECONDS


def main():
  """Run cache check."""
  FLAGS.Parse()

  # Print the Header
  print "Content-type: text/html\n"

  # If file doesn't exist or is older than 5 minutes, create it
  if not os.path.exists(DAILY_FILE) or GetTimeDiff(DAILY_FILE) > 5:
    message = generate_daily_report.CreateDailySummaryString("log.txt")
    utils.WritetoFile(DAILY_FILE, message)

  DumpFile(DAILY_FILE)


if __name__ == "__main__":
  main()
