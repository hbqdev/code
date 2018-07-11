"""Class for parsing the scanstation logs and generating HTML for the email.

This class depends on the TimeRange class for handling data and generating
the time ranges objects the scans are filtered into. It is also responsible
for creating the HTML table string for the log data.
"""

__author__ = ("nguyenmic@google.com (Michael Nguyen)")

import datetime
import logging
import re
import time


class SBSLogParser(object):
  """Parses the scanstation logs."""

  def __init__(self, station, log_file, total_time_range,
               start_capture, end_capture, upload_capture, karnak_error):
    """Args:
         station: the hostname of parsed log file
         log_file: the log file to be parsed
         total_time_range: the time range representing the entire day
         start_capture: string indicating a scan has started
         end_capture: string indicating the scanstation has finished scanning
         upload_capture: string indicating the scan has uploaded
         karnak_error: string indicating a software error
    """

    self.station = station
    self.log_file = log_file
    self.total_time_range = total_time_range
    self.start_capture = start_capture
    self.end_capture = end_capture
    self.upload_capture = upload_capture
    self.karnak_error = karnak_error

  def FormatTimeString(self, total_seconds):
    """Format total_seconds into a string.

    Args:
      total_seconds: total amount of seconds

    Returns:
      Time string
    """
    return time.strftime("%H:%M:%S", time.gmtime(total_seconds))

  def GetLogTime(self, line):
    """Parse the timestamp in the log files.

    Args:
      line: a single line from the log file

    Returns:
      Datetime object
    """
    if not re.match(r"\d+-\d+-\d", line):
      return None

    # Split the timestamp at the beginning of the line
    time_split = re.split(r"-\d{4}\s", line)

    # Create a datetime object
    time_object = datetime.datetime.strptime(time_split[0],
                                             "%Y-%m-%d %H:%M:%S")

    return time_object

  def GenerateTimeblockString(self, time_range):
    """Generate buffered HTML string to write to output file.

    Args:
      time_range: TimeRange object

    Returns:
      Buffered HTML string
    """
    html_string = "<tr><td align = center>%s</td>" % time_range
    html_string += "<td align = center>%s</td>" % time_range.total
    html_string += "<td align = center>%s</td>" % time_range.canceled
    html_string += "<td align = center>%s</td>" % time_range.errors
    html_string += "<td align = center>%s</td>" % (
        self.FormatTimeString(time_range.AverageRigScanTime()))
    html_string += "<td align = center>%s</td>" % (
        self.FormatTimeString(time_range.AverageOperatorScanTime()))
    html_string += "<td align = center>%s</td>" % (
        self.FormatTimeString(time_range.AverageIdletime()))
    html_string += "<td align = center>%s</td></tr>\n" % (
        self.FormatTimeString(time_range.TotalIdleTime()))

    return html_string

  def FilterError(self, time_ranges, start_time):
    """Filters the error into their correct TimeRange objects.

    Args:
      time_ranges: list of TimeRange objects
      start_time: start time of a scan
    """
    # Always add it to total time_range
    self.total_time_range.errors += 1

    for time_range in time_ranges:
      if time_range.TimeisValid(start_time):
        time_range.errors += 1
        return

    logging.warning("Error does not match any filters")

  def FilterScan(self, time_ranges, start_time, end_time, upload_time):
    """Filters the scans into their correct TimeRange objects.

    Args:
      time_ranges: list of TimeRange objects
      start_time: start time of a scan
      end_time: end time of a scan
      upload_time: upload time of a scan
    """
    # Always add it to total time_range
    self.total_time_range.AddScan(start_time, end_time,
                                  upload_time)

    for time_range in time_ranges:
      if time_range.TimeisValid(start_time):
        time_range.AddScan(start_time, end_time, upload_time)
        return

    logging.warning("Scan does not match any filters")

  def ParseLog(self, time_ranges):
    """Parse through a scanstation's log file line by line.

    Args:
      time_ranges: list of time_range objects
    """
    # Indicates whether it has detected a scan has started
    scan_status = 0

    for line in self.log_file:
      if re.search(self.karnak_error, line):
        self.FilterError(time_ranges, self.GetLogTime(line))
        continue

      if re.search(self.start_capture, line):
        if scan_status:
          self.FilterScan(time_ranges, start_time, None, None)
        scan_status = 1
        start_time = self.GetLogTime(line)
        continue

      if re.search(self.end_capture, line):
        if scan_status:
          end_time = self.GetLogTime(line)
          scan_status = 2
        continue

      if re.search(self.upload_capture, line):
        if scan_status == 2:
          scan_status = 0
          upload_time = self.GetLogTime(line)
          self.FilterScan(time_ranges, start_time, end_time, upload_time)

  def GenerateTimeBlockData(self, time_ranges):
    """Generate the timeblock data and corresponding HTML.

    Args:
      time_ranges: list of time ranges to filter log data into

    Returns:
      dictionary of the day's data
    """
    # Reset the class data for the next log parsing.
    for time_range in time_ranges:
      time_range.Reset()

    self.ParseLog(time_ranges)

    daily_data = {}
    html_string = ""

    html_string += "Summary: %s <br>\n" % self.station
    html_string += "<table border='1'>\n"
    html_string += "<tr><th></th><th>Completed</th><th>Canceled</th>"
    html_string += "<th>Errors</th>"
    html_string += "<th>Average Rig Scan Time</th>"
    html_string += "<th>Average Operator Scan Time</th>"
    html_string += "<th>Average Time Between Scans</th>"
    html_string += "<th>Total Idle Time</th></tr>"

    # Filter the log data into different timeblocks
    for time_range in time_ranges:
      daily_data[str(time_range)] = time_range.total
      daily_data[str(time_range) + "_canceled"] = time_range.canceled
      daily_data[str(time_range) + "_error"] = time_range.errors

      html_string += self.GenerateTimeblockString(time_range)

    # Special case for total
    daily_data["Total"] = self.total_time_range.total
    daily_data["Total_canceled"] = self.total_time_range.canceled
    daily_data["Total_error"] = self.total_time_range.errors

    html_string += self.GenerateTimeblockString(self.total_time_range)

    html_string += "</table><br>\n"

    daily_data["html_string"] = html_string

    return daily_data
