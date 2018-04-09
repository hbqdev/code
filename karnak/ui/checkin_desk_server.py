# Copyright 2012 Google Inc. All Rights Reserved.

"""Twisted HTTP server viewer for checkin desks."""
__author__ = "kwc@google.com (Ken Conley)"

import optparse
import sys
import os
import errno

from twisted.internet import reactor
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twisted.web.server import Site
from twisted.web.static import File

from resources import desk_config
from ui import resource_adapter


if __name__ == '__main__':
  parser = optparse.OptionParser("usage: %prog [options] [config-file]")
  parser.add_option("--debug",
                    action="store_true", dest="debug", default=False,
                    help="Enable debug HTTP server logging")
  options, args = parser.parse_args()
  if len(args) > 1:
    parser.error("Only one config file may be specified")
  if not args:
    parser.error("Please specify config file")
  debug = options.debug
  if debug:
    log.startLogging(sys.stdout)
  else:
    try:
      os.makedirs("static/logs")
    except OSError as e:
      if e.errno == errno.EEXIST:
        pass
      else:
        raise
    log.startLogging(DailyLogFile("log.txt", "static/logs"))

  if args:
    print "Loading configuration from", args[0]
    config = desk_config.LoadConfigFromFile(args[0])

  base_directory = config.base_directory
  root = File(base_directory)

  root.putChild(
      "checkin",
      resource_adapter.ConfigObjectHandler(config, path="checkin"))

  reactor.listenTCP(8081, Site(root))
  print "created reactor"
  reactor.run()
