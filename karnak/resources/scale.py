
# Copyright 2012 Google Inc. All Rights Reserved.

"""Resource API for printers."""

from drivers import scale

from resources import katamari


def Register(factory):
  factory.RegisterFromDict("DymoScale", DymoScale.FromDict)
  factory.RegisterFromDict("FakeScale", FakeScale.FromDict)


class Scale(katamari.KatamariResource):
  """Abstract Scale resource."""

  def __init__(self):
    super(Scale, self).__init__()

  def GetActions(self):
    return {"weigh": self.Weigh}

  def Weigh(self):
    """Returns weight of object currently on scale.

    Returns:
      Weight of object.
    """
    raise NotImplementedError


class DymoScale(Scale):
  """Dymo Scale resource."""

  def __init__(self, dymo_usb_path):
    super(DymoScale, self).__init__()
    self._dymo = scale.Dymo(dymo_usb_path)

  def Weigh(self):
    """Returns weight of object currently on scale.

    Returns:
      Weight of object.
    """
    return {"weight": self._dymo.GetWeight(), "units": "grams"}

  @staticmethod
  def FromDict(raw_config):
    s = DymoScale(raw_config["handle"])
    katamari.FromDict(s, raw_config)
    return s


class FakeScale(Scale):
  """Fake Scale resource."""

  def __init__(self):
    super(FakeScale, self).__init__()

  def GetActions(self):
    return {"weigh": self.Weigh}

  def Weigh(self):
    """Returns weight of object currently on scale.

    Returns:
      Weight of object.
    """
    return {"weight": 1234.0, "units": "grams"}

  @staticmethod
  def FromDict(raw_config):
    s = FakeScale()
    katamari.FromDict(s, raw_config)
    return s
