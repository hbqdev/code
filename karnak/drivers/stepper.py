import socket
import struct
import sys
import threading
import time

import serial


class FlexController(object):

  def __init__(self, port):
    self.s = serial.Serial(port)
    self.s.timeout = .01
    self.mutex = threading.Lock()

  def xchange(self, snd, cnt):
    self.perty(snd)

    with self.mutex:
      self.s.write(snd)
      # Give the controller some time to respond, this will be cached
      time.sleep(.1)

      # we could try to catch the case where we get no response
      rx = self.s.read(cnt)


    self.perty(rx)
    return rx

  def setClockwise(self, port, val):
    if (val):
      self.xchange(struct.pack("<6s", "D%dCWHi" % port), 0)
    else:
      self.xchange(struct.pack("<6s", "D%dCWLO" % port), 0)

  def perty(self, package):
    print [repr(b) for b in package]

  def getStatus(self, port):
    """Return the remaining steps for the port."""
    state = self.xchange('V', 20)
    if 'B' not in state:
      return 0
    i = state.index('B')
    # There is an implicit assumption here that we only have
    # the one motor active.
    if (state[i+1] == str(port)):
      return struct.unpack(">I", chr(0)+state[i+2:i+5])
    return 0

  def package(self, cmd, port, val):
    """Create the packet type that the 3d3 is expecting."""
    estep = struct.pack(">I", val)
    package = struct.pack("> 3s", "%s%dM" % (cmd, port))
    package += estep[1:]
    return package

  def step(self, port, steps):
    self.xchange(self.package("I", port, steps), 10)
    print self.getStatus(port)

  def setSpeed(self, port, speed):
    self.xchange(self.package("S", port, speed), 10)
    print self.getStatus(port)

  def emergencyStop(self):
    """ Stop all steppers connected to the controller. """
    for i in range(1, 5):
      package = struct.pack("<6s", "E%dHALT" % (i))
      self.xchange(package, 10)

  def halt(self, port):
    """ Brings the stepper to an immediate halt."""
    package = struct.pack("<6s", "E%dHALT" % (port))
    self.xchange(package, 10)

class FlexStepper(object):

  def __init__(self, controller, id):
    self.controller = controller
    self.id = id

  def step(self, steps):
    self.controller.step(self.id, steps)

  def setSpeed(self, speed):
    self.controller.setSpeed(self.id, speed)

  def setClockwise(self, flag):
    self.controller.setClockwise(self.id, flag)

  def getStatus(self):
    return self.controller.getStatus(self.id)

  def halt(self):
    self.controller.halt(self.id)


class ImsStepper(object):
  """Driver for EtherIP MDrive Stepper."""

  def __init__(self, ip_address, port, init_cmds):
    """Initalize stepper.

    Args:
      ip_address: IP address of stepper on local network
      port: TCP/IP port open for commands (usually 503)
      init_cmds: list of commands to send to stepper
    """
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((ip_address, port))
    self.setDefaults(init_cmds)

  def close(self):
    self.sock.close()

  def setDefaults(self, init_cmds):
    for command in init_cmds:
      cmd_str = "%s\r\n" % (command)
      print "Sending Stepper command: %s" % (command)
      self.sendCommand(cmd_str)

  def sendCommand(self, str_command):
    sent = self.sock.send(str_command)
    if sent == 0:
      raise RuntimeError("Socket connection broken to IMS")
    elif sent != len(str_command):
      raise RuntimeError("Not able to send the whole command")

  def setVelocity(self, velocity):
    self.sendCommand("SL %d\r\n" % velocity)

  def setAcceleration(self, acceleration):
    self.sendCommand("A %d\r\n" % acceleration)

  def setDeceleration(self, deceleration):
    self.sendCommand("D %d\r\n" % deceleration)

  def setMaxVelocity(self, velocity):
    self.sendCommand("VM %d\r\n" % velocity)
    self.sendCommand("VI %d\r\n" % velocity/2)

  def moveRelative(self, steps):
    self.sendCommand("MR %d\r\n" % steps)

  def move(self, accel, decel, maxv, steps):
    self.setAcceleration(accel)
    self.setDeceleration(decel)
    self.setMaxVelocity(maxv)
    self.moveRelative(steps)

  def emergencyStop(self):
    self.setVelocity(0)

if __name__ == "__main__":
  # Rewritten by willmartin to use for cal
  steps = int(sys.argv[1])

  print "Moving Stepper to %s in 72 steps for cal" % steps

  # Use empty init_cmds to keep last used config
  stepper = ImsStepper("192.168.33.1", 503, {})

  for i in range(72):
    stepper.moveRelative(steps/72)
    time.sleep(1.5)

  print "Done"

