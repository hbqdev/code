# Copyright 2012 Google Inc. All Rights Reserved.

"""Resource API for printers."""

from resources import katamari

HEADER = "DataOps"
DEFAULT_LP_HANDLE = "/dev/usb/lp0"


def Register(factory):
  factory.RegisterFromDict("LpPrinter", LpPrinter.FromDict)
  factory.RegisterFromDict("FakePrinter", FakePrinter.FromDict)


class Printer(katamari.KatamariResource):
  """Abstract Printer resource."""

  def __init__(self):
    super(Printer, self).__init__()

  def GetActions(self):
    return {"print": self.Print}

  def Print(self, value):
    """Prints barcode value."""
    raise NotImplementedError

  @staticmethod
  def FromDict(raw_config):
    s = Printer()
    katamari.FromDict(s, raw_config)
    return s


class LpPrinter(Printer):
  """lp-based Printer resource."""

  def __init__(self):
    super(LpPrinter, self).__init__()
    self._handle = DEFAULT_LP_HANDLE

  def Print(self, value):
    """Prints barcode value."""
    with open(self._handle, 'wt') as f:
      f.write("N\nq650\nA80,10,0,2,2,1,N,\"%s\"\nB80,50,0,1A,3,8,100,B,\"%s\"\nP\n"
              % (HEADER, value) )
      f.flush()

  @staticmethod
  def FromDict(raw_config):
    s = LpPrinter()
    katamari.FromDict(s, raw_config)
    if "handle" in raw_config:
      s._handle = raw_config["handle"]
    return s


class FakePrinter(Printer):
  """Fake Printer resource."""

  def __init__(self):
    super(FakePrinter, self).__init__()

  def Print(self, value):
    """Prints barcode value."""
    print "Fake print", value

  @staticmethod
  def FromDict(raw_config):
    s = FakePrinter()
    katamari.FromDict(s, raw_config)
    return s
