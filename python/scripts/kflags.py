"""This module is used to define and parse command line flags.

 This module defines a *distributed* flag-definition policy: rather than
an application having to define all flags in or near main(), each python
module defines flags that are useful to it.  When one python module
imports another, it gains access to the other's flags.  (This is
implemented by having all modules share a common, global registry object
containing all the flag information.)

Please see Google's python-gflags for the inspiration of this project.

This module uses the python argparse package for all the heavy lifting.
As such, flags are defined in the AddArgument() method by using
argparse's add_argument syntax:

http://docs.python.org/2/library/argparse.html#the-add-argument-method

Furthermore, flags can be ordered into conceptual groupings by using
the DefineArgumentGroup and AddArgumentToGroup() methods.

Example Usage:

  import kflags

  FLAGS = kflags.FLAGS
  kflags.AddArgument("--foo",type=int,default=17)
  kflags.DefineArgumentGroup("name", "Name parameters")
  kflags.AddArgumentToGroup("name", "--first",type=str,default="Ben")
  kflags.AddArgumentToGroup("name", "--last",type=str,default="Bitdiddle")

  def main():
    FLAGS.Parse()
    print "%s %s has %d foo." % (FLAGS.first, FLAGS.last, FLAGS.foo)

  if __name__ == "__main__":
    main()

This will produce the following help file:

  usage: example.py [-h] [--foo FOO] [--first FIRST] [--last LAST]

  optional arguments:
    -h, --help     show this help message and exit
    --foo FOO

  name:
    Name parameters

    --first FIRST
    --last LAST
"""

import argparse


class FlagValues(object):
  def __init__(self):
    self.parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    self.groups = {}

  def Parse(self):
    self.parser.parse_args(namespace=FLAGS)


class ArgumentGroupError(Exception):
  """Exception for errors with Argument Groups."""
  pass

# The Global flag object
FLAGS = FlagValues()


def AddArgument(*args, **kwargs):
  FLAGS.parser.add_argument(*args, **kwargs)


def DefineArgumentGroup(group, description):
  """Create logical argument group for related flags.

  Args:
    group: Name of argument group to be displayed
    description: Optional description for Argument group. Use None to skip

  Raises:
    ArgumentGroupError: if flag group is created multiple times
  """
  if group in FLAGS.groups:
    raise ArgumentGroupError("Duplicate kflags group '%s'" % group)
  else:
    arg_group = FLAGS.parser.add_argument_group(group, description)
    FLAGS.groups[group] = arg_group


def AddArgumentToGroup(group, *args, **kwargs):
  if group not in FLAGS.groups:
    raise ArgumentGroupError("Missing kflags group '%s'" % group)
  else:
    FLAGS.groups[group].add_argument(*args, **kwargs)


def SetDefaults(group, **kwargs):
  """Override default value already defined."""
  if not group:
    FLAGS.parser.set_defaults(**kwargs)
  elif group not in FLAGS.groups:
    raise ArgumentGroupError("Missing kflags group '%s'" % group)
  else:
    FLAGS.groups[group].set_defaults(**kwargs)




