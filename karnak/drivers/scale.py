"""Driver code to read weight information from Dymo USB scale.

TODO(nguyenmic): This should probably be rewritten using PyUSB instead
of reading directly from the USB port using ctypes.
"""
import ctypes

DYMO_USB_PATH = "/dev/usb/hiddev0"


def ToInt(byte_array, offset, length):
  """Convert the byte information into integer values.

  Args:
    byte_array: the byte array to parse
    offset: the offset in the byte array to begin information
    length: the length of the byte array to convert

  Returns:
    Integer value of the byte array
  """
  result = 0
  for x in range(0, length):
    result |= (ord(byte_array[x + offset]) << 8 * x)
    signed_number = ctypes.c_int(result & 0xFFFFFFFF).value
  return int(signed_number)


class Dymo(object):
  """Opens up Dymo USB scale port for reading."""

  def __init__(self, dymo_usb_path):
    """Open up the Dymo USB port for reading.

    Args:
      dymo_usb_path: USB port location
    """
    self._dymo_usb_path = dymo_usb_path

  def GetWeight(self):
    """Get the weight information from USB port.

    NOTE: The first byte array value will always be set to zero.
    The actual weight value will always be in the second byte array.

    Returns:
      Weight from Dymo USB scale.
    """
    with open(self._dymo_usb_path, "rb") as dymo_stream:
      for _ in range(0, 2):
        byte_array = list(dymo_stream.read(8))
        value = ToInt(byte_array, 4, 4)

      return value


def main():
  """Print out twenty readings from the Dymo USB scale."""
  dymo = Dymo(DYMO_USB_PATH)

  for _ in range(0, 20):
    print "Current weight: %d" % dymo.GetWeight()


if __name__ == "__main__":
  main()
