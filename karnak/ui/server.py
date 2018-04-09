# Copyright 2012 Google Inc. All Rights Reserved.

"""Websocket and Twisted HTTP server viewer for Scan Stations."""
__author__ = "arshan@google.com (Arshan Poursohi)"

import json
import optparse
import os
import sys

import Image

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from twisted.python import log
from twisted.python.logfile import DailyLogFile

from resources.websocket import BroadcastServerFactory, \
                                BroadcastServerProtocol
from resources import scanner
from resources import scanner_config
from ui import resource_adapter

# TODO(arshan): wrap this in resources.websocket
from autobahn.websocket import listenWS

class ScanBroadcaster(object):
  def __init__(self, server):
    self.server = server

  # TODO(kwc): change message to progress
  # TODO(kwc): move to thread so this doesn't stuff the scan thread.
  def ScanCallback(self, filename, metadata):
    """
    Args:
      filename: Path to captured image.
      metadata: Dictionary of key/value metadata.
    """
    if not os.path.exists(filename):
      print >> sys.stderr, "Cannot send thumbnail, capture to [%s] failed" % filename
      return
    thumb_filename = filename[:-4] + '.tn.jpg'
    img = Image.open(filename)
    img.thumbnail((320,240), Image.ANTIALIAS)
    img.save(thumb_filename)

    with open(thumb_filename, 'rb') as f:
      data = f.read()
    print "sending thumbnail", filename
    print "scan metadata", metadata
    content = json.dumps({'msgbase64': data.encode("base64"),
                          'msgmetadata': metadata})
    self.server.broadcastRaw(content)
    print "sent thumbnail"


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

  # TODO(arshan): permission not granted, sort out why
  # log.startLogging(DailyLogFile.fromFullPath("/scan/log/daily.log"))

  print "Loading configuration from", args[0]
  config = scanner_config.LoadConfigFromFile(args[0])

  ServerFactory = BroadcastServerFactory

  socketserver = ServerFactory("ws://localhost:9000",
                               debug = debug,
                               debugCodePaths = debug)

  socketserver.protocol = BroadcastServerProtocol
  socketserver.setProtocolOptions(allowHixie76 = True)
  listenWS(socketserver)

  base_directory = config.base_directory
  root = File(base_directory)

  # Extract the scanners from the config.  This is a bridging hack for now as
  # the config, in theory, should auto-configure the server.
  scanners = [s for s in config.resources if isinstance(s, scanner.Scanner)]

  # Wire in the websocket callbacks.
  scan_broadcaster = ScanBroadcaster(socketserver)
  for s in scanners:
    s.SetScanCallback(scan_broadcaster.ScanCallback)

  root.putChild(
      "config",
      resource_adapter.ConfigObjectHandler(config, path="config"))

  reactor.listenTCP(8080, Site(root))
  reactor.run()
