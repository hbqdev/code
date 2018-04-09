# Copyright 2012 Google Inc. All Rights Reserved.

"""Packs up files into a single file, e.g., tarball."""
__author__ = "kwc@google.com (Ken Conley)"

import datetime
import os
import time

import pytz

from resources import katamari
from resources import errors
from resources import executors

PACIFIC = pytz.timezone("US/Pacific")


def Register(factory):
  factory.RegisterFromDict("Tarball", Tarball.FromDict)


class Packer(katamari.KatamariResource):
  def __init__(self):
    katamari.KatamariResource.__init__(self)


class Tarball(Packer):

  def __init__(self, output_dir):
    Packer.__init__(self)
    self._output_dir = output_dir

  @staticmethod
  def FromDict(raw_config):
    p = Tarball(raw_config["output_directory"])
    katamari.FromDict(p, raw_config)
    return p

  def GetOutputName(self, capture_dir):
    return "%s.tar" % os.path.basename(capture_dir)

  def Create(self, capture_dir, swivel_manifest,
             tarball_name=None, working_dir=None, executor=None, exclude=None):
    """Creates tarball for upload.

    Args:
      capture_dir: Directory where images were captured.  Must only contain
          data from single capture.
      swivel_manifest: ScanObject instance.  Must have scan station and KID
          information.
      tarball_name: Override default tarball name (<dirname>.tar).
      working_dir: Optional working directory for tarball generation.
      executor: Override executor used to execute external processes.
      exclude: Glob pattern for any files to exclude.
    Returns:
      Tarball filename.
    Raises:
      errors.ConfigError: if swivel manifest is not valid.
      errors.InternalError: If capture_dir does not exist.
    """
    if executor is None:
      executor = executors.CheckedSubprocessExecutor
    if not capture_dir:
      raise errors.InternalError("Capture dir does not exist: " % capture_dir)

    if not os.path.exists(self._output_dir):
      os.makedirs(self._output_dir)
    output_name = (self.GetOutputName(capture_dir)
                   if not tarball_name else tarball_name)
    output_name = os.path.join(self._output_dir, output_name)
    # Have to convert to absolute path as we will set working dir.
    output_name = os.path.abspath(output_name)
    rel_capture_dir = (os.path.relpath(capture_dir, working_dir)
                       if working_dir else capture_dir)
    if exclude:
      cmd = " ".join(["tar", "cf", output_name, rel_capture_dir,
                     "--exclude=" + exclude])
    else:
      cmd = " ".join(["tar", "cf", output_name, rel_capture_dir])
    executor(cmd, cwd=working_dir)
    return output_name

  def GetSwivelAssetId(self, swivel_manifest):
    """Gets string id to use for asset generation.

    Args:
      swivel_manifest: ScanObject instance.  Must have scan station and KID
          information.
    Returns:
      Identifier to use for swivel asset.  Used in folder and tarball name.
    Raises:
      errors.ConfigError: if swivel manifest is not valid.
    """
    datestr = GetCompactDateString()
    if not swivel_manifest.HasField("scan_station"):
      raise errors.ConfigError("Missing required scan_station metadata")
    ss_id = swivel_manifest.scan_station.id
    # Additional 'K' precedes the Katamari ID in case the specification adds
    # more fields.
    return "%s-%s-K-%s-2d" % (datestr, ss_id, swivel_manifest.katamari_id)

  def GetCalibrationAssetId(self, swivel_manifest, suffix):
    """Gets string id to use for calibration asset generation.

    Args:
      swivel_manifest: ScanObject instance.  Must have scan station and KID
          information.
    Returns:
      Identifier to use for swivel asset.  Used in folder and tarball name.
    Raises:
      errors.ConfigError: if swivel manifest is not valid.
    """
    datestr = GetCompactDateString()
    if not swivel_manifest.HasField("scan_station"):
      raise errors.ConfigError("Missing required scan_station metadata")
    ss_id = swivel_manifest.scan_station.id
    # Additional 'K' precedes the Katamari ID in case the specification adds
    # more fields.
    return "%s-%s-K-%s-%s" % (datestr, ss_id,
                             swivel_manifest.katamari_id,
                             suffix)


def GetCompactDateString():
  """Gets timestamp in compact date format."""
  utc_time = pytz.UTC.localize(datetime.datetime.utcnow())
  pac_time = utc_time.astimezone(PACIFIC)
  is_dst = time.localtime().tm_isdst
  if is_dst:
    return pac_time.strftime("%Y%m%d-%Hd%M%S")
  else:
    return pac_time.strftime("%Y%m%d-%Hs%M%S")
