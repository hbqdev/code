import json
from time import gmtime, strftime

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol

class BroadcastSocketProtocol(WebSocketServerProtocol):

  def onOpen(self):
    self.factory.register(self)

  def onMessage(self, msg, binary):
    if not binary:
      self.factory.broadcast("'%s' from %s" % (msg, self.peerstr))

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)


class BroadcastSocketFactory(WebSocketServerFactory):
  """
  Simple broadcast server broadcasting any message it receives to all
  currently connected clients.
  """

  def __init__(self, url, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.tickcount = 0

  def register(self, client):
    if not client in self.clients:
      print "registered client " + client.peerstr
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      print "unregistered client " + client.peerstr
      self.clients.remove(client)

# I want to change this to take a dict, ... then jsonify it
  def broadcast(self, msg):
    print "broadcasting prepared message '%s' .." % msg
    content = json.dumps({'msg:html':strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),'snapshot:src':msg})
    preparedMsg = self.prepareMessage(content)
    for c in self.clients:
      c.sendPreparedMessage(preparedMsg)
      print "prepared message sent to " + c.peerstr
