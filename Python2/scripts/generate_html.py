"""Generate dailies and calibrations html page.

"""

__author__ = ("nguyenmic@google.com (Michael Nguyen)")

import logging

import kflags
import stations
import utils

FLAGS = kflags.FLAGS
kflags.SetDefaults("stations", type=["prod", "canary"])
kflags.AddArgument("--daily_filename", type=str,
                   default="dailies.html",
                   help="specify the daily html filename")
kflags.AddArgument("--calibration_filename", type=str,
                   default="calibrations.html",
                   help="specify the calibration html filename")


def CreateHyperlink(station_ip, tn, img, file_type):
  """Generates the HTML hyperlink string.

  Args:
    station_ip: Scanstation IP
    tn: tn file name
    img: img file name
    file_type: "calibration" or "daily"

  Returns:
    HTML hyperlink string
  """
  url_src = "<td><a href=http://%s:8080/%s/%s>" % (
      station_ip, file_type, img)
  img_src = "<img src=http://%s:8080/%s/%s></a></td>" % (
      station_ip, file_type, tn)

  return url_src + img_src


def Position1through3ForDaily(station_dict, camera_pos):
  """Camera position 1-3 case for daily page.

  Args:
    station_dict: Dictionary of scanstation hostnames and IPs
    camera_pos: Camera position

  Returns:
    Buffered HTML string
  """
  sorted_stations = stations.GetSortedHostnames(station_dict)

  string_to_write = ""

  for x in range(0, 380, 20):
    string_to_write += "<tr>"

    tn = "%i-%03i.tn.jpg" % (camera_pos * 10, x)
    img = "%i-%03i.jpg" % (camera_pos * 10, x)

    for station in sorted_stations:
      line = CreateHyperlink(station_dict[station],
                             tn, img, "daily")
      string_to_write += line

    string_to_write += "</tr>"

  return string_to_write


def Position1through3ForCalibration(station_dict, camera_pos):
  """Camera position 1-3 case for calibration page.

  Args:
    station_dict: Dictionary of scanstation hostnames and IPs
    camera_pos: Camera position

  Returns:
    Buffered HTML string
  """
  sorted_stations = stations.GetSortedHostnames(station_dict)

  string_to_write = ""

  for x in range(0, 360, 10):
    string_to_write += "<tr>"

    tn = "%i-%03i.tn.jpg" % (camera_pos * 10, x)
    img = "%i-%03i.jpg" % (camera_pos * 10, x)

    for station in sorted_stations:
      line = CreateHyperlink(station_dict[station],
                             tn, img, "calibration")
      string_to_write += line

    string_to_write += line

  return string_to_write


def Position4Exception(station_dict, file_type):
  """Special Case for Camera Position 4.

  Args:
    station_dict: Dictionary of scanstation hostnames and IPs
    file_type: "calibration" or "daily"

  Returns:
    Buffered HTML string
  """
  sorted_stations = stations.GetSortedHostnames(station_dict)

  string_to_write = ""

  string_to_write += "<tr>"

  tn = "40-270.tn.jpg"
  img = "40-270.jpg"

  for station in sorted_stations:
    line = CreateHyperlink(station_dict[station],
                           tn, img, file_type)
    string_to_write += line

  string_to_write += line

  return string_to_write


def GenerateFile(station_dict, file_type):
  """Generates html file for scanstations.

  Args:
    station_dict: Dictionary of scanstation hostnames and IPs
    file_type: "calibration" or "daily"

  Returns:
    Buffered HTML string
  """
  sorted_stations = stations.GetSortedHostnames(station_dict)

  string_to_write = ""

  for camera_pos in range(1, 5):
    string_to_write += "<b>Camera Position %s</b>" % camera_pos
    string_to_write += "<table>"

    string_to_write += "<tr>"

    for station in sorted_stations:
      string_to_write += "<th>Station %s</th>" % station

    string_to_write += "</tr>"
    string_to_write += "<tr>"

    tn = "empty-%i-000.tn.jpg" % (camera_pos * 10)
    img = "empty-%i-000.jpg" % (camera_pos * 10)

    for station in sorted_stations:
      line = CreateHyperlink(station_dict[station],
                             tn, img, "calibration")
      string_to_write += line

    string_to_write += "</tr>"

    if camera_pos == 4:
      line = Position4Exception(station_dict, file_type)
    else:
      if file_type == "daily":
        line = Position1through3ForDaily(station_dict, camera_pos)
      else:
        line = Position1through3ForCalibration(station_dict, camera_pos)

    string_to_write += line

    string_to_write += "</table>"

  return string_to_write


def main():
  FLAGS.Parse()

  utils.InitializeLogging()

  scan_stations = stations.Stations()
  servers = scan_stations.GetStationIPs()

  html_string = GenerateFile(servers, "daily")
  logging.info("Generating %s page", FLAGS.daily_filename)
  utils.WritetoFile(FLAGS.daily_filename, html_string)

  html_string = GenerateFile(servers, "calibration")
  logging.info("Generating %s page", FLAGS.calibration_filename)
  utils.WritetoFile(FLAGS.calibration_filename, html_string)

if __name__ == "__main__":
  main()
