#!/usr/bin/python

import sys
import cmd
import time
import os
import couleur
import curses
import ConfigParser
import pexpect
from twisted.internet import reactor

config = ConfigParser.SafeConfigParser( )

def importConfig(filename):
  config.read( filename )

def init_flexscan():
  flexscan = pexpect.spawn(config.get("Scan", "FlexScan3D"))
  flexscan.expect('interactive')

def do_3d_scan():
  KatamariID = raw_input("Please provide Katamari ID: ")
  ConfirmID = raw_input("Once more to verify: ")
  if (KatamariID == ConfirmID):
    print "Looks good, proceeding with scan"
  init_flexscan()
  flexscan.sendline('capture %s %s %s'%(projectName, scanName, calibration))


class CommandProcessor(cmd.Cmd):
  """Basic implementation of a command line, all calls should route out from here."""

  def do_sh(self, line):
    "Run a shell command"
    output = os.popen(line).read()
    sh.green(output)
    self.last_output = output

  def do_reset(self, line):
    "Reset the underlying server"
    reactor.crash()
    reactor.run()

  def do_scan (self, line):
    "Use Flexscan3D to complete a 3D scan of the object."
    do_3d_scan()
    print "Scan complete."

  def do_status (self, line):
    "Show current status of the workstation."
    print "Scan in progress."

  def do_quit (self,line ):
    "exit karnak"
    sh.red("Later.\n\n")
    exit(0)

  def do_EOF(self, line):
    return True

  def default(self,line):
    "the default behavior is to execute in the shell"
    #os.execle("pwd","",os.environ)
    sh.red("this is not a full shell environment, careful.\n")
    self.do_sh(line)


sh = couleur.Shell(indent=4)
for f in sys.argv[1:]:
  importConfig(f)

cmd.Cmd.prompt = "%s> "%config.get("Station", "name")

# could use this to allow init.py .... execfile(f)

if __name__ == '__main__':
  CommandProcessor().cmdloop()
