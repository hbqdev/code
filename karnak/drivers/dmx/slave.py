
class DmxSlave(object):
  """A Slave device on a DMX chain. """

  def __init__(self, start, length):
    self.start, self.length = start, length
    self.values = [0] * self.length

  def set(self, chan, value):
    """set the value of this channel to value (relative channel number)"""
    self.values[chan] = value

  def get(self, chan):
    return self.values[chan]

  def pack(self, buf):
    """modify the passed buffer in place"""
    for index in range(self.length):
      buf[self.start+index] = self.values[index]

  def __str__(self):
    return "dmx_slave: start=%d, length=%d>" % (self.start, self.length)
