# -*- coding: utf-8 -*-

""" driver for an XBee light for small interior spaces,
i.e. the insides of shoes.  can handle up to 9 shoelights as written,
but technically could do 15.

physical shoelight documentation:
https://docs.google.com/a/google.com/document/d/1q_HaoOpsgbvCq7mRHovZtNYEA3yJ8ElOrSwn4anYzjg
 """

__author__ = "katydek@google.com (Katie Dektar)"


import commands
import serial
import time


OFF = 0
ON = 1


class ShoeLight():

  # connect to the USB port
  def __init__(self, port):
    self._port = port
    self._serial = serial.Serial('/dev/' + self._port, 9600)

  def __str__(self):
    return "ShoeLight: on=%d" % (self.isOn)

  # note: can only have up to 9 shoelights with this code!
  # to add more shoelights, add their checksums below.
  def on(self, shoe_id):
    checksum = ''
    if shoe_id == 1:
      checksum = '1A'
    if shoe_id == 2:
      checksum = '19'
    if shoe_id == 3:
      checksum = '18'
    if shoe_id == 4:
      checksum = '17'
    if shoe_id == 5:
      checksum = '16'
    if shoe_id == 6:
      checksum = '15'
    if shoe_id == 7:
      checksum = '14'
    if shoe_id == 8:
      checksum = '13'
    if shoe_id == 9:
      checksum = '12'
    print "turning shoelight on"
    self.sendCommand("7E 00 10 17 01 00 00 00 00 00 00 00 00 50 0%s 02 44 31 05 %s"
                     % (shoe_id, checksum))
    self.isOn = ON


  def off(self, shoe_id):
    checksum = ''
    if shoe_id == 1:
      checksum = '1B'
    if shoe_id == 2:
      checksum = '1A'
    if shoe_id == 3:
      checksum = '19'
    if shoe_id == 4:
      checksum = '18'
    if shoe_id == 5:
      checksum = '17'
    if shoe_id == 6:
      checksum = '16'
    if shoe_id == 7:
      checksum = '15'
    if shoe_id == 8:
      checksum = '14'
    if shoe_id == 9:
      checksum = '13'
    print "turning shoelight off"
    self.sendCommand("7E 00 10 17 01 00 00 00 00 00 00 00 00 50 0%s 02 44 31 04 %s"
                     % (shoe_id, checksum))
    self.isOn = OFF


  #  use the serial port to send the command
  def sendCommand(self, command):
    self._serial.write(bytearray.fromhex(command))


if __name__ == "__main__":

  light = ShoeLight()

  print "toggling the shoe light"
  while True:
    light.on()
    print "light on!\n"
    time.sleep(5)
    light.off()
    print "light off\n"
    time.sleep(5)
