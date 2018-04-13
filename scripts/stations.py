#!/usr/bin/python

"""Class to help manage katamari scan stations.

The Stations class abstracts knowledge about the Katamari Scan Stations to allow
future scripts to interact with targeted stations. For example, scripts could
backup configuration files from only production machines in Mountain View.

The associated configuration data is stored in stations.yaml

Josh Weaver <jweaver@google.com>
"""

import argparse
import logging
import os.path
import re
import sys
import yaml

import kflags
import utils

# Full path if running on scan station
YAML_PATH = os.path.expanduser("~/scanning-ops/scripts/stations.yaml")
YAML_FILENAME = "stations.yaml"
# Keyword associated with IP root in YAML file
LOCATION_IP_ROOT = "IP_root"

STATION_TYPE_CHOICES = ["prod", "canary", "checkin", "server",
                        "dev", "notdev", "all"]


class ExpandPaths(argparse.Action):
  """Expand relative paths as argparse action."""

  def __call__(self, parser, namespace, values, option_string=None):
    if isinstance(values, basestring):
      output = os.path.abspath(os.path.expanduser(values))
    else:
      output = [os.path.abspath(os.path.expanduser(x)) for x in values]
    setattr(namespace, self.dest, output)

FLAGS = kflags.FLAGS

kflags.DefineArgumentGroup("stations", None)
kflags.AddArgumentToGroup("stations", "--yaml_path", type=str,
                          default=YAML_PATH, action=ExpandPaths,
                          help="Full path to stations.yaml")
kflags.AddArgumentToGroup("stations", "--type", type=str,
                          nargs="+", choices=STATION_TYPE_CHOICES,
                          default=["prod"],
                          help="Desired station type(s)")


def GetSortedHostnames(stations):
  """Generates sorted list of scan station hostnames.

  Args:
    stations: Dictionary of stations, as returned by GetStationIPs

  Returns:
    Sorted list of scanstation hostnames
  """
  convert = lambda text: int(text) if text.isdigit() else text
  sort_key = lambda item: [convert(c) for c in re.split("([0-9]+)", item)]
  return sorted(stations, key=sort_key)


class Stations(object):
  """Process scan station info stored in stations.yaml config file."""

  def __init__(self, yaml_file=None):
    """Inits Station with values from yaml.

    Args:
      yaml_file: yaml file containing scannery information

    TODO(nguyenmic): Make yaml_file a required parameter
    """
    if not yaml_file:
      yaml_file = FLAGS.yaml_path
    if os.path.isfile(os.path.expanduser(yaml_file)):
      yaml_filename = os.path.expanduser(yaml_file)
      logging.debug("Using YAML %s", yaml_filename)
    elif os.path.isfile(YAML_FILENAME):
      yaml_filename = YAML_FILENAME
      logging.debug("Using YAML %s", yaml_filename)
    else:
      logging.fatal("Unable to find YAML file %s", yaml_filename)
      # TODO(nguyenmic): replace with exceptions
      sys.exit(1)

    self.stations_config = yaml.load(open(yaml_filename))

  def _GenerateIPs(self, scannery, root, stations):
    """Construct dict of station names and corresponding IP addresses."""
    # TODO(nguyenmic): Find a smart way to handle 172.17.26.10[1,3] hostnames
    ips = {}
    for station in stations:
      ip = "%s.%s" % (root, station)
      name = "%s%d" % (scannery.lower(), station)
      ips[name] = ip
    return ips

  def GetLocationRootIP(self, location):
    """Returns the root IP of a scannery location.

    Args:
      location: location of the scannery

    Returns:
      location root IP
    """
    return self.stations_config[location][LOCATION_IP_ROOT]

  def GetStationIPs(self, location="SBS", station_types=None):
    """Returns dict of station names and IP addresses for desired stations.

    TODO(nguyenmic): change `location` to remove default value

    Args:
      location: name of scannery, such as SBS or CAS.
      station_types: list of scanstation types. [prod, dev, etc]
    In both of the above, "all" returns all options

    Returns:
    dictionary of station name to IP address mappings.
    {'sbs11': '172.26.17.11', etc}
    """
    if not station_types:
      station_types = FLAGS.type
    target_ips = {}
    for station_type in station_types:
      if station_type not in STATION_TYPE_CHOICES:
        logging.warning("Unknown station type: %s", station_type)
        continue

      for scannery in self.stations_config:
        if scannery == location or location == "all":
          root = self.stations_config[scannery][LOCATION_IP_ROOT]

          if station_type in ["prod", "notdev", "all"]:
            target_ips.update(self._GenerateIPs(
                scannery, root, self.stations_config[scannery]["prod"]))
          if station_type in ["canary", "notdev", "all"]:
            target_ips.update(self._GenerateIPs(
                scannery, root, self.stations_config[scannery]["canary"]))
          if station_type in ["checkin", "notdev", "all"]:
            target_ips.update(self._GenerateIPs(
                scannery, root, self.stations_config[scannery]["checkin"]))
          if station_type in ["server", "notdev", "all"]:
            target_ips.update(self._GenerateIPs(
                scannery, root, self.stations_config[scannery]["server"]))
          if station_type in ["dev", "all"]:
            target_ips.update(self._GenerateIPs(
                scannery, root, self.stations_config[scannery]["dev"]))

    return target_ips

  def PrettyPrintYaml(self):
    """Debugging function to display station yaml."""
    print yaml.dump(self.stations_config, default_flow_style=False)


def main():
  """Simple debug output if run stand alone."""
  # Example of using argparse parent
  FLAGS.Parse()

  utils.InitializeLogging()

  test_station = Stations()
  print "You selected type == %s" % (FLAGS.type)
  # Display yaml
  test_station.PrettyPrintYaml()

if __name__ == "__main__":
  main()
