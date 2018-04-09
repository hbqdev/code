from twisted.internet import protocol, reactor
from threading import Timer
import socket
import random
import time

messages = ["",
            "Hey, man. Whatcha doing?",
            "Just checking out a Python example on Runnable.",
            "Oh, yeah? What is it about?",
            "Some stuff about Twisted and chat servers. Come check it out.",
            "Sweet!"]
messages.reverse()

transports = {}

class Chat(protocol.Protocol):
  def connectionMade(self):
    self._peer = self.transport.getPeer()
  def dataReceived(self, data):
    username_and_message = data.split(":")
    username = username_and_message[0]
    message = username_and_message[1]
    transports[username] = self.transport
    for key in transports.keys():
      if key != username:
        transports[key].write(username+" says: "+message)

class ChatFactory(protocol.Factory):
  def buildProtocol(self, addr):
    return Chat()

def testChat(username):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('127.0.0.1', 1236))
  while messages:
    s.send(username+":"+messages.pop())
    data = s.recv(1024)
    print "["+username+"]:", data
    time.sleep(1)
  s.close()

Timer(0.5, testChat, args=["Jimmy Struthers"]).start()
Timer(0.5, testChat, args=["Tyrone Jackson"]).start()
reactor.listenTCP(8080, ChatFactory())
reactor.run()
