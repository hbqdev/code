#!/usr/bin/env python
# Copyright 2012 Google Inc. All Rights Reserved.

"""Manually upload tarballs to bigstore"""
__author__ = "kwc@google.com (Ken Conley)"

import optparse
import os

from resources import scanner_config
from tests import mock_hardware

mock_hardware.MockAll()

if __name__ == '__main__':
  parser = optparse.OptionParser()
  parser.add_option("--folder", dest="folder",
                    help="folder", metavar="FILE")
  options, args = parser.parse_args()
  if not args:
    parser.error("please specify input file(s)")

  config = scanner_config.LoadDefaultConfig()
  for store in config.storage:
    print "Uploading %s to [%s]" % (args, store)
    kid = 'K00000000'
    print "WARNING, using fake KID", kid
    # Only use different APIs so we can test actual APIs.
    if len(args) > 1:
      store.UploadFiles(kid, args, folder=options.folder)
    elif len(args) == 1:
      if options.folder:
        target_path = os.path.join(options.folder, os.path.basename(args[0]))
      store.UploadFile(kid, args[0], target_path=target_path)

