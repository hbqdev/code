# -*- coding: utf-8 -*-

""" Dmx driver for the Chauvet DMX 4 LED power controller.

    For more information please see http://www.chauvetlighting.com/dmx-4-led/

    This driver supports only the 4 channel mode, extend as necessary. """

__author__ = "arshan@google.com (Arshan Poursohi)"

from dmx.slave import DmxSlave
from dmx.master import EntecUsbPro

class ChauvetDmx4Led(DmxSlave):

  def allOn(self):
    self.allBanks(True)

  def allOff(self):
    self.allBanks(False)

  def allBanks(self, value):
    for i in range(1,5):
      self.setBank(i, value)

  def setBank(self, bank, value):
    """Turn on or off the bank of plugs.
       Note that the index refers to the silk screened indices on the device 
       and is therefore 1-based. 
    """
    
    if (bank < 1 or bank > 4):
      return
    self.set(bank-1, 255 if value else 0)

  def __init__(self, start):
    DmxSlave.__init__(self, start, 4)

  def __str__(self):
    return "DMX LED: bank1=%d, bank2=%d, bank3=%d, bank4=%d" % (self.get(0), self.get(1), self.get(2), self.get(3))


if __name__ == "__main__":

  controller = EntecUsbPro('/dev/dmx0')
  dut = ChauvetDmx4Led(1)
  controller.append(dut)

  cnt = 0
  period = 8096

  while (True):

    dut.setBank(1, False)
    dut.setBank(2, False)
    dut.setBank(3, False)
    dut.setBank(4, False)

#    dut.setBank(1, True if cnt > period/2 else False)
#    dut.setBank(2, True if cnt > period/3 else False)
#    dut.setBank(3, True if cnt > period/4 else False)
#    dut.setBank(4, True if cnt > period/5 else False)

    controller.send()

   # too noisy. print dut

    cnt += 1
    if cnt > period :
      cnt = 0
