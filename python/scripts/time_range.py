"""Class for storing and manipulating time range scan data.

All time variables are passed into this class as Datetime objects for easy
date and time comparison and manipulation.

NOTE: This class depends on the SBSLogParser class for passing in data.
"""
import datetime


class TimeRange(object):
  """Stores and processes data from scanstation logs."""

  def __init__(self, start_hour, start_minute, end_hour, end_minute,
               all_day=False):
    self.start = datetime.time(start_hour, start_minute)
    self.end = datetime.time(end_hour, end_minute)
    self.all_day = all_day

    self.Reset()

  def Reset(self):
    """Resets the class variables so it's not reused for the next log parsing.
    """
    # The previous end time of a scan needs to be stored because idle time
    # calculation is handled as the start time of a new scan subtracted
    # from the end time of a previous scan
    self.last_scan_end_time = 0

    self.total = 0
    self.canceled = 0
    self.errors = 0

    # Time variables are stored as seconds

    # Rig scan time is the actual scan time of the rig
    self.total_rig_scan_time = 0

    # Operator scan time is the time between the operator clicking
    # the "Start" and "Done" UI buttons
    self.total_operator_scan_time = 0

    # Idle time is the time between the end of the last scan and start
    # of the next scan
    self.total_idle_time = 0

  def AddScan(self, start_time, end_time, upload_time):
    """Add scan to TimeRange object.

    Note: All time variables are datetime objects.

    Args:
      start_time: start time of the scan
      end_time: end time of the scan
      upload_time: upload time of the scan
    """
    # If end_time is None, then it's assumed to be a canceled scan.
    if not end_time:
      self.canceled += 1
      return

    self.total += 1
    self.total_operator_scan_time += (upload_time -
                                      start_time).total_seconds()
    self.total_rig_scan_time += (end_time -
                                 start_time).total_seconds()

    if self.last_scan_end_time:
      self.total_idle_time += (start_time -
                               self.last_scan_end_time).total_seconds()
    self.last_scan_end_time = upload_time

  def AverageOperatorScanTime(self):
    """Compute the average operator scan time.

    Returns:
      Average scan operator time in minutes
    """
    # If no scans, return 0 to avoid dividing by 0
    if self.total == 0:
      return 0

    return self.total_operator_scan_time/self.total

  def AverageRigScanTime(self):
    """Compute the average rig scan time.

    Returns:
      Average rig scan time in minutes
    """
    if self.total == 0:
      return 0

    return self.total_rig_scan_time/self.total

  def AverageIdletime(self):
    """Compute the average idle time.

    Returns:
      Average idle time in minutes
    """
    # Self.total is checked against 1 because idle time calculation looks
    # at the interval between scans NOT the total amount of scans
    if self.total > 1:
      return self.total_idle_time/(self.total - 1)

    return self.total_idle_time

  def TotalIdleTime(self):
    """Returns the total idle time.

    Total idle time = Available time in a time range subtracted by
                     the time spent scanning

    Returns:
      total idle time in minutes
    """
    # Generic year, month, and day values are used here to create a
    # valid datetime.datetime object to get the total idle time.
    shift_start_time = datetime.datetime(2014, 1, 1, self.start.hour,
                                         self.start.minute, 0)
    shift_end_time = datetime.datetime(2014, 1, 1, self.end.hour,
                                       self.end.minute, 0)

    total_time = (shift_end_time - shift_start_time).total_seconds()

    return total_time - self.total_operator_scan_time

  def TimeisValid(self, start_time):
    """Checks to see if the scan time is valid for the TimeRange class.

    Args:
      start_time: the start time of the scan

    Returns:
      True, if scan time is between the self.start and self.end times
      False, if scan time is not between the self.start and self.end times
    """
    if start_time.time() > self.start and start_time.time() <= self.end:
      return True

    return False

  def __str__(self):
    """Generate the time range string."""
    start_string = self.start.strftime("%I:%M %p")
    end_string = self.end.strftime("%I:%M %p")

    if end_string == "11:59 PM":
      end_string = "End of Day"

    time_range_string = "%s - %s" % (start_string, end_string)

    if self.all_day:
      return "Total"

    return time_range_string
