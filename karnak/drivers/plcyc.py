# -*- coding: utf-8 -*-

""" Dmx driver for the Phillips Selecon PLCyc led cyc light.

    For more information please see http://www.strandlighting.com

    This driver supports only the 8 bit mode, extend as necessary. """

__author__ = "willmartin@google.com (Alex Martin)"

from dmx.slave import DmxSlave
from dmx.master import EntecUsbPro

class PLCyc(DmxSlave):

  def __init__(self, start):
    DmxSlave.__init__(self, start, 8)
    self.set(7, 0)

  def __str__(self):
    return "PLCyc: intensity=%d, red=%d, green=%d, blue=%d, white=%d" % (self.get(0), self.get(1), self.get(2), self.get(3), self.get(4))

  def setRed(self, value):
    self.set(1, value)

  def setGreen(self, value):
    self.set(2, value)

  def setBlue(self, value):
    self.set(3, value)

  def setWhite(self, value):
    self.set(4, value)

  def setIntensity(self, value):
    self.set(0, value)

  def allOn(self):
    self.allColors(255)
    self.setIntensity(255)

  def allOff(self):
    self.allColors(0)
    self.setIntensity(0)

  def allColors(self, value):
    for i in range(0,4):
      self.set(i, value)


if __name__ == "__main__":

  controller = EntecUsbPro('/dev/dmx')
  cyc1 = PLCyc(5)
  controller.append(cyc1)
  cyc2 = PLCyc(13)
  controller.append(cyc2)

  cnt = 0
  period = 18096

  cyc1.setIntensity(255)
  cyc2.setIntensity(255)

  while (True):

    cyc1.setRed(255 if cnt > period/5 else 0)
    cyc1.setGreen(255 if cnt > period/4 else 0)
    cyc1.setBlue(255 if cnt > period/3 else 0)
    cyc1.setWhite(255 if cnt > period/2 else 0)

    cyc2.setRed(255 if cnt > period/5 else 0)
    cyc2.setGreen(255 if cnt > period/4 else 0)
    cyc2.setBlue(255 if cnt > period/3 else 0)
    cyc2.setWhite(255 if cnt > period/2 else 0)

    controller.send()

   # too noisy.  print cyc1

    cnt += 1
    if cnt > period :
      cnt = 0
