# Copyright 2012 Google Inc. All Rights Reserved.

"""Resource API for steppers."""

import math
import time

from drivers import stepper
from resources import errors
from resources import katamari


def Register(factory):
  factory.RegisterFromDict("ImsStepper", ImsStepperWrapper.FromDict)
  factory.RegisterFromDict("FakeStepper", FakeStepper.FromDict)


class Stepper(katamari.KatamariResource):
  """Abstract Stepper resource."""

  def __init__(self):
    super(Stepper, self).__init__()
    self._segments = 0

  def GetActions(self):
    return {"step_once": self.StepOneSegment,
            "step_once_back": self.StepOneSegmentBack,
            "full_turn": self.FullTurn,
            "half_turn": self.HalfTurn}

  def SetSegments(self, segments):
    """Sets number of segments to divide steps into.

    Args:
      segments: Number of segments.
    """
    self._segments = segments

  def StepOneSegment(self):
    """Moves hardware stepper one segment."""
    raise NotImplementedError

  def StepOneSegmentBack(self):
    """Moves hardware stepper back one segment."""
    raise NotImplementedError

  def Step(self, steps):
    """Moves hardware stepper.

    Args:
      steps: Number of steps to increment.
    """
    raise NotImplementedError

  def FullTurn(self):
    raise NotImplementedError

  def HalfTurn(self):
    raise NotImplementedError


class ImsStepperWrapper(Stepper):
  """Stepper Motor Class for the Katamari IMS Steppers."""

  def __init__(self, steps, address, port, delay_per_step, init_cmds):
    super(ImsStepperWrapper, self).__init__()
    self._steps = steps
    self._total_steps = 0
    self._delay_per_step = delay_per_step
    try:
      self._stepper = stepper.ImsStepper(address, port, init_cmds)
    except:
      self._stepper = None
      print "Cannot connect to stepper at %s:%d" % (address, port)

  @staticmethod
  def FromDict(raw_config):
    s = ImsStepperWrapper(raw_config["steps"],
                          raw_config["address"],
                          raw_config["port"],
                          raw_config["delay_per_step"],
                          raw_config["init_cmds"])
    katamari.FromDict(s, raw_config)
    return s

  def __str__(self):
    return (super(ImsStepperWrapper, self).__str__() +
            "\ntotal steps: %s"
            "\nsteps per rev %s" % (self._total_steps,
                                    self._steps))

  def SetSegments(self, cnt):
    """Sets the number of segments that are captured per 360 degree rotation."""
    self._segments = cnt

  def StepOneSegment(self):
    self.StepSegment(True)

  def StepOneSegmentBack(self):
    self.StepSegment(False)

  def StepSegment(self, forward):
    """Steps one segment forwards or backwards.

    Args:
      forward: Boolean, whether to step forward or not.
    """
    if not self._segments:
      raise errors.InternalError("Segments not set")
    step_count = self._steps / self._segments
    if forward:
      self.Step(step_count)
    else:
      self.Step(-step_count)
    # TODO(arshan): gross approximation, we should monitor the step count from the motor.
    # Negative step counts create reversed direction rotation
    time.sleep(math.fabs(step_count * self._delay_per_step))

  def Step(self, cnt):
    if self._stepper is None:
      raise errors.InternalError("ImsStepper not initialized,"
                                 "will not actually step %d" % cnt)
    else:
      self._stepper.moveRelative(cnt)
    self._total_steps += cnt

  def FullTurn(self):
    self.Step(self._steps)

  def HalfTurn(self):
    self.Step(self._steps/2)

  def TurnDegrees(self, degrees):
    self.Step(degrees/360 * self._steps)


class FakeStepper(Stepper):
  """Fake stepper for use in test captures for a noop turntable."""

  @staticmethod
  def FromDict(raw_config):
    s = FakeStepper()
    katamari.FromDict(s, raw_config)
    return s

  def __str__(self):
    return (super(FakeStepper, self).__str__() +
            "\nposition: fake")

  def StepOneSegment(self):
    pass

  def StepOneSegmentBack(self):
    pass

  def Step(self, cnt):
    pass
