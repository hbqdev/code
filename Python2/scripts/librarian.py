#!/usr/bin/python

""" Script to make backup imagery accessible

Persephone holds ops raw backups for the past few weeks.  This
script makes those accessible from the web, providing the only
means of backups that some folks with restricted access can get.

@author willmartin@google.com
"""

print("Content-type: text/html\n")

import cgi
import cgitb
import os
import re
import shutil
import tarfile

rootloc = "/scan/"

cgitb.enable()

host = os.environ["SERVER_NAME"]

def dirprint ( dirloc ):
  files = os.listdir(rootloc + dirloc)

  files.sort()

  print("<h3>Index of %s</h3>" % (dirloc, "Backups")[dirloc == ""])
  if dirloc != "":
    print("<a href=\"?loc=%s\">Go Back</a><br>" % (os.path.normpath(dirloc + "../")))

  for d in files:
    if re.search("\.tar", d):
      print("%s: <a href=\"?loc=%s%s\">Download</a> <a href=\"?pull=%s%s\">Unpack</a><br>" % (d, dirloc, d, dirloc, d))
    elif os.path.isdir(rootloc + dirloc + d):
      print("<a href=\"?loc=%s%s\">%s</a> [%s items]<br>" % (dirloc, d, d, len(os.listdir(rootloc + dirloc + d))))

def recprint ():
  files = os.listdir("/tmp/www/unpacked/")

  files.sort()

  for d in files:
    if os.path.isdir("/tmp/www/unpacked/" + d):
      print("<a href=\"http://%s/tmp/unpacked/%s\">%s</a><br>" % (host, d, d))

def errorprint ():
  print("""

<h2>Error</h2>
<br>
There appears to have been an error (or maybe you weren't playing nice?).  Use your browsers back button to go back or you can go <a href="?">home</a><br>
""" )


form = cgi.FieldStorage()

print("""
<html>

<head><title>The Librarian</title></head>

<body>

    <h2> Welcome to the Librarian </h2>
""")

#print("Running on %s" % (os.environ["SERVER_NAME"]))

print("""
<div id=\"recent\" style=\"width:400px;float:left;\">
<h3>Recently Unpacked</h3>
""")

recprint()

print("</div>")

print("<div id=\"content\" style=\";width:550px;float:left;\">")

if "pull" in form:
  pull = form.getfirst("pull")
  if re.search("\.\.", pull):
    errorprint()
  else:
    tarball = tarfile.open(rootloc + pull)
    tarball.extractall(path="/tmp/www/unpacked/")
    print("<meta http-equiv=\"REFRESH\" content=\"0;url=http://%s/tmp/unpacked/%s\">" % (host, re.split("\.", (re.split("/", pull)[-1]))[0]))
else:
  if "loc" in form:
    loc = form.getfirst("loc")
    if re.search("\.\.", loc):
      errorprint()
    elif re.search("\.tar", loc):
        shutil.copyfile((rootloc + loc), "/tmp/www/%s" % (re.split("/", loc)[-1]))
        print("<meta http-equiv=\"REFRESH\" content=\"0;url=http://%s/tmp/%s\">" % (host, re.split("/", loc)[-1]))
        dirprint(os.path.dirname(loc))
    elif loc == ".":
      dirprint("")
    else:  
      dirprint("%s/" % loc)
  else:
    dirprint("")

print("</div>")

print("""

</body>

</html>
""")
