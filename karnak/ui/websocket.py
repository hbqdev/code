# Copyright 2012 Google Inc. All Rights Reserved.

"""Websocket and Twisted HTTP server viewer for Scan Stations."""
__author__ = "arshan@google.com (Arshan Poursohi)"

import json
import optparse
import os
import sys
import time
import errno

import Image

from twisted.internet import reactor
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twisted.web.server import Site
from twisted.web.static import File

from resources import scanner
from resources import scanner_config
from ui import resource_adapter

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import listenWS


# TODO:
# - check if autobahn is already in third party, else ... maybe drop the websocket thing?
# - centralize the websocket delivery of live content
# - camera goes to a resource

camera = '/dev/v4l/by-id/usb-046d_0823_9ABA64A0-video-index0'
builtin = '/dev/v4l/by-id/usb-Chicony_Electronics_Co.__Ltd._Integrated_Camera-video-index0'
cnt = 0

class BroadcastServerProtocol(WebSocketServerProtocol):

  def onOpen(self):
     self.factory.register(self)

  def onConnect(self, request):
     print request.params
     #if not 'sid' in request.params:
     #  raise HTTPException(401, "not authorized")
     # do something with the sid to map back to the resource ...
     return WebSocketServerProtocol.onConnect(self, request)

  def onMessage(self, payload, isBinary):
     if not isBinary:
        msg = "{} from {}".format(payload.decode('utf8'), self.peer)
        self.factory.broadcast(msg)


  def connectionLost(self, reason):
     WebSocketServerProtocol.connectionLost(self, reason)
     self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
   """
   Simple broadcast server broadcasting any message it receives to all
   currently connected clients.
   """

   def __init__(self, url, debug = False, debugCodePaths = False):
      WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
      self.clients = []

   def registerResource(self, resource):
      print "registered id : %s" % resource.GetName()

   def register(self, client):
      if not client in self.clients:
         print "registered client " + client.peer
         self.clients.append(client)

   def unregister(self, client):
      if client in self.clients:
         print "unregistered client " + client.peer
         self.clients.remove(client)

   def broadcast(self, msg):
      val = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
      content = json.dumps({'msg:html': val, 'testing:newmason': msg})
      preparedMsg = self.prepareMessage(content)
      for c in self.clients:
         c.sendPreparedMessage(preparedMsg)

   def broadcastRaw(self, msg):
      preparedMsg = self.prepareMessage(msg)
      for c in self.clients:
         c.sendPreparedMessage(preparedMsg)


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

    preview = filename.startswith('static/preview')
    
    thumb_filename = filename[:-4] + '.tn.jpg'
    img = Image.open(filename)
    if (preview):
      img.thumbnail((640,480), Image.ANTIALIAS)
    else:
      img.thumbnail((320,240), Image.ANTIALIAS)
    img.save(thumb_filename)

    with open(thumb_filename, 'rb') as f:
      data = f.read()
    print "sending thumbnail", filename
    print "scan metadata", metadata
    content = json.dumps({'msgbase64': data.encode("base64"), 
                          'msgmetadata': metadata,
                          'preview': 1 if preview else 0 })
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
    config = scanner_config.LoadConfigFromFile(args[0])
  else:
    config = scanner_config.LoadDefaultConfig()

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
