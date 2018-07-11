"""Grabs the amount of 3d scans by grepping though tmp logs.

TODO(nguyenmic): This will be rewritten once John Sheu finishes the new 3d
                 logging system.
"""
import datetime
import logging
import subprocess
import time

import kflags
import utils

FLAGS = kflags.FLAGS

# Dictionary of 3d Station hostnames and IPs
STATIONS_3D = ["sbs21", "sbs22", "sbs23"]
# Path to 3d scan directories
SCAN_PATH = "/scan/"
# Log filename
LOG_PATH = "/tmp/"
# Dictionary Keys
COMPLETED = "completed"
CANCELED = "canceled"
AVERAGE_TIME = "average_time"


def GetScanLogs(station_ip, log_name):
  """SSH into a 3d scanstation to find scan count by grepping logs.

  Args:
    station_ip: 3d scanstation ip
    log_name: The name of the log to parse

  Returns:
    String of log information
  """
  user_at_station = "katamari@%s" % station_ip
  cmd = ["ssh", user_at_station, "grep", "\"Full scan\"",
         log_name, "|", "cut", "-d:", "-f2-"]

  try:
    scan_logs = utils.CheckSubprocessCall(cmd)
  except subprocess.CalledProcessError as ssh_error:
    logging.error("Station %s unreachable", station_ip)
    logging.error(ssh_error)
    return None

  return scan_logs


def AppendSummaryString(daily_data, num_stations):
  """Create the summary data for all 3d stations.

  Args:
    daily_data: Dictionary of 3d scans data
    num_stations: Number of 3d stations

  Returns:
    String of daily 3d scan data
  """
  daily_summary = ("==========<br>"
                   "Daily Summary: 3D Scans<br>"
                   "<table border=1>"
                   "<tr><th></th><th>Completed</th><th>Canceled</th></tr>"
                   "<tr><td>Total</td><td>%s</td><td>%s</td></tr>"
                   "</table><br>"
                   "Average completed scans per rig: %s<br>"
                   "==========<br><br>"
                   % (daily_data[COMPLETED], daily_data[CANCELED],
                      daily_data[COMPLETED] / num_stations))
  return daily_summary


def ParseDictionaryToHTML(scan_data):
  """Convert scan data to html string.

  Args:
    scan_data: Dictionary of 3d scan data

  Returns:
    HTML string of 3d scan data
  """
  return ("<table border='1'><tr><th></th>"
          "<th>Completed</th><th>Canceled</th>"
          "<th>Average Time</th></tr>"
          "<tr><td>Total</td><td>%s</td><td>%s</td><td>%s</td></tr>"
          "</table><br>"
          % (scan_data[COMPLETED],
             scan_data[CANCELED],
             scan_data[AVERAGE_TIME]))


def ParseLogToDictionary(scan_logs):
  """Convert scan log information to scan_data dictionary.

  Args:
    scan_logs: Scanstation log data

  Returns:
    Dictionary of scan data
  """
  scan_data = {COMPLETED: 0,
               CANCELED: 0,
               AVERAGE_TIME: 0}

  for entry in scan_logs.splitlines():
    entry_list = entry.split()

    if "finished" in entry:
      scan_data[COMPLETED] += 1

      # The last list element contains the scan time
      scan_time = entry_list[-1]
      scan_data[AVERAGE_TIME] += float(scan_time.strip("s)"))
    elif "failed" in entry:
      scan_data[CANCELED] += 1
    else:
      continue

  # If there's no scan completed, skip the average_time computation.
  if not scan_data["completed"]:
    return scan_data

  scan_data[AVERAGE_TIME] = (float(scan_data[AVERAGE_TIME])
                               / scan_data[COMPLETED])
  scan_data[AVERAGE_TIME] = str(datetime.timedelta(seconds=round(
      scan_data[AVERAGE_TIME])))
  return scan_data


def Generate3dHTMLString(stations_list=STATIONS_3D):
  """Generate a html string from 3D data string.

  Args:
    stations_list: list of station hostnames

  Returns:
    HTML string of 3d scan data
  """
  html_string = ""
  daily_data = {COMPLETED: 0,
                CANCELED: 0}

  for station in stations_list:
    logging.debug(station)
    html_string += "Summary: %s<br>" % station

    date_today = time.strftime("%Y%m%d")
    log_name = "%sscanner-main.*.log.INFO.%s*" % (LOG_PATH, date_today)

    scan_logs = GetScanLogs(station, log_name)
    if not scan_logs:
      html_string += "Log File Not Found/Unreachable<br>"
      html_string += ("<b>Note: Station could temporarily be powered down"
                      " for maintenance service.</b><br><br>")
      continue

    scan_data = ParseLogToDictionary(scan_logs)
    html_string += ParseDictionaryToHTML(scan_data)

    daily_data[COMPLETED] += scan_data[COMPLETED]
    daily_data[CANCELED] += scan_data[CANCELED]

  return AppendSummaryString(daily_data, len(stations_list)) + html_string


def main():
  """Print out 3d scans information."""
  FLAGS.Parse()
  utils.InitializeLogging()

  print Generate3dHTMLString()

if __name__ == "__main__":
  main()
