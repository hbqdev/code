#!/usr/bin/python
"""CGI script that gives a live preview of the scanstations' scans.

This script depends on the following two javascript files:
  1: /scanning-ops/www/js/jquery.js
  2: /scanning-ops/www/js/socketed.js

NOTE: This script belongs in the /usr/lib/cgi-bin/ directory.
"""
import kflags
import stations

# The different camera positions of a scanstation
CAMERA_POSITIONS = ("front", "ortho", "top")

FLAGS = kflags.FLAGS
kflags.SetDefaults("stations", type=["prod", "canary", "dev"])


def HTMLDump(sorted_stations, stations_dict, camera_positions):
  """Generates the websockets to create the live preview images.

  Args:
    sorted_stations: list of sorted scanstations
    stations_dict: dictionary of scanstation hostnames and IPs
    camera_positions: camera positions of a scanstations

  Returns:
    HTML string with javascript
  """
  html_string = """<!DOCTYPE html><html>\
<META HTTP-EQUIV="Refresh" CONTENT="600"><head>\
<script type="text/javascript"src="/js/socketed.js"></script>\
<script src="/js/jquery.js"></script>\
<script type="text/javascript">\
var logpane = null;\
window.onload = function() {\
logpane = document.getElementById('log');"""

  for station_ip in stations_dict.values():
    html_string += "spawn_socket('%s');" % station_ip

  html_string += "}</script></head><body><table>"

  stations_per_row = len(sorted_stations)/2

  row_list = [[station for station in sorted_stations[:stations_per_row]],
              [station for station in sorted_stations[stations_per_row:]]]

  for station_list in row_list:
    html_string += "<tr>"
    for station in station_list:
      html_string += "<td><a href=http://%s:8080>" % stations_dict[station]
      html_string += "<b>%s</b></a></td>" % station
    html_string += "</tr>"

    for position in camera_positions:
      html_string += "<tr>"
      for station in station_list:
        station = stations_dict[station].replace(".", "_")
        html_string += "<td><img id='%s-%s_camera' " % (station, position)
        html_string += "src='n.jpg' /></td>"
      html_string += "</tr>"

  html_string += """</table>\
<noscript>You must enable JavaScript</noscript>\
<button id="log_toggle" onclick="button_toggle('log', 'log_toggle')">\
hide logs</button>\
<pre id="log" style="height: 50em; overflow-y: scroll;\
background-color: #aaa;"></pre>\
</body></html>"""

  return html_string


def main():
  """Generate and print the HTML string needed to display the live preview."""
  FLAGS.Parse()

  scan_stations = stations.Stations()
  stations_dict = scan_stations.GetStationIPs()
  sorted_stations = stations.GetSortedHostnames(stations_dict)

  # Print the Header
  print "Content-type: text/html\n"
  print HTMLDump(sorted_stations, stations_dict, CAMERA_POSITIONS).strip("\t")

if __name__ == "__main__":
  main()
