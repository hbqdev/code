# -*- coding: utf-8 -*-

""" Python binding for the custom katamari controller on LCAv2 """

__author__ = "arshan@google.com (Arshan Poursohi)"

import time
import socket


class Controller(object):

  def __init__(self, ip_address):
    self._defaultport = 503
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((ip_address, self._defaultport))
    self.setDefaults()
    
  def close(self):
    self.sock.close()

  def setDefaults(self):
    pass

  def sendCommand(self, str_command):
    sent = self.sock.send(str_command)
    if sent == 0:
      raise RuntimeError("[Controller] Socket connection broken")
    elif sent != len(str_command):
      raise RuntimeError("[Controller] Not able to send the whole command")    

  # TODO(arshan): decent command language for the controller, so we can use it for other tasks too.
  def crosshairs(self, val):
    if val:
      self.sendCommand("H")
    else:
      self.sendCommand("h")
      
  def __str__(self):
    return "KController"

if __name__ == "__main__":

  print "toggling the crosshairs"
  
  controller = Controller("192.168.101.2")

  while True:  
    controller.crosshairs(True)
    time.sleep(5)
    controller.crosshairs(False)
    time.sleep(5)
  
