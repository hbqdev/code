# Copyright 2012 Google Inc. All Rights Reserved.

"""Processes scan station configuration."""
__author__ = "kwc@google.com (Ken Conley)"

from resources import katamari


# TODO(kwc): move to resources.station
class Station(katamari.KatamariResource):
  """Scan station metadata."""

  __slots__ = ["touchscreen",
               "model",
               "base_directory",
               "capture_directory",
               "calibration_directory",
               "daily_directory",
               "test_directory",
               "status"]

  def __init__(self):
    katamari.KatamariResource.__init__(self)
    self.touchscreen = False
    self.model = None
    self.capture_directory = None
    self.calibration_directory = None
    self.daily_directory = None
    self.test_directory = None
    self.status = None

  @staticmethod
  def FromDict(raw_config):
    """Creates new instances from dictionary.

    Args:
      raw_config: Configuration in dict representation.

    Returns:
      Station config
    """
    station = Station()
    for a in ["touchscreen",
              "model",
              "capture_directory",
              "calibration_directory",
              "test_directory"]:
      setattr(station, a, raw_config[a])
    station.daily_directory = raw_config.get("daily_directory", "daily")
    katamari.FromDict(station, raw_config)
    return station

  def __str__(self):
    return "Name: %s\nModel: %s\nTouchscreen: %s" % (self.name,
                                                     self.touchscreen,
                                                     self.model)
