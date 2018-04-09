import os
import ctypes
import time
import threading

def toInt(offset, length, arr):
  result = 0
  for x in range(0,length):
    result |= (ord(arr[x+offset]) << 8*x)
    signed_number = ctypes.c_int(result&0xFFFFFFFF).value
  return signed_number

class HandleMonitor(threading.Thread):
  def __init__(self, fh, cbck):
    threading.Thread.__init__(self)
    self.fh = fh
    self.cbck = cbck
    self._keep_running = True

  def shutdown(self):
    self._keep_running = False

  def run(self):
    while _keep_running:
            # so you want to add a timeout of say 100ms, and notice <24 chars ...
      x = list(self.fh.read(24))
      enum =  toInt(0,1,x)
      magic = toInt(1,3,x)
      vtype = toInt(16,2,x)
      code =  toInt(18,2,x)
      value = toInt(20,4,x)
      if code != 0:
        self.cbck(enum, magic, vtype, code, value);

class ShuttleExpress(object):

  def __init__(self, handle):
    self.shuttle = []
    self.button = []
    self.ring = []
    self.prev = 0
    self.monitor = HandleMonitor(
            open(handle, "rb"),
            self.handleReadout)
    self.monitor.start()

  def registerShuttleCallback(self, cbck):
    self.shuttle.append(cbck)

  def registerRingCallback(self, cbck):
    self.ring.append(cbck)

  def registerButtonCallback(self, cbck):
    self.button.append(cbck)

  def handleReadout(self, enum, magic, vtype, code, value):
    if vtype == 1:
      if value == 1:
        for c in self.button:
          c(code-260)
    elif vtype == 2:
      if code == 8:
        for c in self.ring:
          c(value)
      elif code == 7:
        if (self.prev != value):
          self.prev = value
          for c in self.shuttle:
            c(value)
    # elif code == 7:


def bcallback(b):
  print "Button! %d" % b

def scallback(b):
  print "shuttle/ring %d" % b

if __name__ == "__main__":

f = ShuttleExpress("/dev/input/by-id/usb-Contour_Design_ShuttleXpress-event-if00")
f.registerButtonCallback(bcallback)
f.registerRingCallback(scallback)
f.registerShuttleCallback(scallback)

# just wait for stuff to happen ...
while True:
  time.sleep(5)
  print " -----"
