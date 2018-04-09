import serial
import numpy
import struct

class DmxMaster(object):
  def __init__(self, port):
    self.s = serial.Serial(port)
    self.buf = numpy.zeros((128,), dtype='B')
    self.devices = []

  def append(self, device):
    self.devices.append(device)

  def send(self):
    """ Just print to screen, since we are a dummy implementation. """
    print join(":", self.buf)

class MockDmxMaster(DmxMaster):

  def __init__(self, port):
    print "Mock Dmx is ignoring %s port" % port
    self.buf = [0] * 128
    self.devices = []

class EntecUsbPro(DmxMaster):
  """ Specific implementation of DmxMaster for the Entec Usb Pro controller.
      For more information see http://www.enttec.com/index.php?main_menu=Products&prod=70304&show=description """

  def send(self):
    for device in self.devices:
      device.pack(self.buf)

    msg = struct.pack("<BBH 128s B",
      0x7e, 6, 128,
      self.buf.tostring(),
      0xe7
    )

    self.s.write(msg)
