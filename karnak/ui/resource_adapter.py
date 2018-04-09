# Copyright 2012 Google Inc. All Rights Reserved.

"""Twisted Resource handler adapters for KatamariResources"""
__author__ = "kwc@google.com (Ken Conley)"

import json
import os
import threading

from twisted.web import resource

from resources import auth_config
from resources import camera
from resources import credential
from resources import desk_config
from resources import errors
from resources import scanner_config
from upload import oauth2_service

COMBINED_AUTH_SCOPE = "%s %s" % (oauth2_service.SCOPE_BIGSTORE_FULL_CONTROL,
                                 oauth2_service.SCOPE_XAPI)


# Whitelists which attributes of the config we serve.
DEFAULT_TOP_LEVEL = ["resources"]
CONFIG_MAP = {
    auth_config.AuthConfig: ["credentials", "storage"],
    desk_config.DeskConfig: ["resources", "credentials", "storage"],
    scanner_config.ScannerConfig: ["resources", "scanners", "credentials", "storage"],
    }


class ConfigObjectHandler(resource.Resource):
  isLeaf = False
  # TODO(arshan): Make the stylesheet configurable?
  _HEAD_HTML = "<html><head><link rel='stylesheet' href='css/touchscreen.css' />"

  def __init__(self, config, config_object=None, path=""):
    resource.Resource.__init__(self)
    self.config = config
    self.config_object = config_object
    self.path = path

  def SetHeaders(self, request):
    request.setHeader("Access-Control-Allow-Origin", "*")
    request.setHeader("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
    request.setHeader("X-Requested-With", "XMLHttpRequest")

  def getRawConfig(self):
    if self.config_object is None:
      return self.config.raw_config
    elif type(self.config_object) == list:
      return [x.name for x in self.config_object]
    else:
      return self.config_object.raw_config

  def getChild(self, name, request):
    config = self.config

    # TODO(arshan): remove this hack once the UI is local again and we can fix the damn thing.
    name = name.replace("scanners", "resources")

    if not name:
      return self
    elif self.config_object is None:
      if name in CONFIG_MAP.get(self.config.__class__, DEFAULT_TOP_LEVEL):
        path = os.path.join(self.path, name)
        return ConfigObjectHandler(config, getattr(config, name), path)
    elif type(self.config_object) == list:
      matches = [x for x in self.config_object if x.name == name]
      if len(matches) == 1:
        obj = matches[0]
        handler = HANDLERS.get(obj.__class__, ConfigObjectHandler)
        return handler(config, obj, self.path + "/" + name)
    elif name in self.config_object.GetActions():
      return ActionHandler(config, self.config_object, self.path, name)
    else:
      raise Exception("no child %s" % name)

  def renderChildren(self, children):
    result = ""
    for name in children:
      path = os.path.join(self.path, name)
      result += "<li><a href='/%s'>%s</a></li>" % (path, name)
    return result

  def renderForm(self, name, action):
    return ("<form action='%s/%s' method='POST'>"
            "<input type=submit value='%s' />"
            "</form>" % (name, action, action))

  def render_OPTIONS(self, request):
    self.SetHeaders(request)
    return ""

  def render_GET(self, request):
    # Check if the request wants one of the special types that we handle.
    # TODO(arshan): Consider support for others, yaml, xml ...
    # TODO(arshan): Replace this with a proper loop that finds the first
    #               supported Accept type.
    requested_types = request.getAllHeaders()["accept"].split(":")
    if "application/json" in requested_types:
      return self.render_JSON(request)

    self.SetHeaders(request)
    children = None
    config_object = None
    if self.config_object is None:
      children = CONFIG_MAP.get(self.config.__class__, DEFAULT_TOP_LEVEL)
      config_object = self.config
    elif type(self.config_object) == list:
      children = [x.name for x in self.config_object]
    else:
      config_object = self.config_object

    result = "%s" % self._HEAD_HTML
    if children:
      result += self.renderChildren(children)
    if config_object:
      result += "<pre>%s</pre>" % config_object
      actions = config_object.GetActions()
      if actions:
        result += "<h2>Actions</h2>"
        for action in sorted(actions):
          result += self.renderForm(config_object.name, action)
    return result

  def render_POST(self, request):
    return "This resource has no support for POST."

  def render_PUT(self, request):
    return "This resource has no support for PUT."

  def render_DELETE(self, request):
    return "This resource has no support for DELETE."

  # Custom HTML generators
  def render_HELP(self, request):
    return "This resource has no help info."

  def render_JSON(self, request):
    raw_config = self.getRawConfig()
    request.setHeader("Content-Type", "application/json; charset=UTF-8")
    request.setHeader("Access-Control-Allow-Origin", "*")
    request.setHeader("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept")
    request.setHeader("X-Requested-With", "XMLHttpRequest")
    return json.dumps(raw_config)


class ActionHandler(ConfigObjectHandler):

  def __init__(self, config, config_object, path, action):
    ConfigObjectHandler.__init__(self, config, config_object, path)
    self.action_name = action

  def render_GET(self, request):
    self.SetHeaders(request)
    if self.action_name == "status":
      request.setHeader("Content-Type", "application/json; charset=UTF-8")
      if self.config_object.status:
        return json.dumps(self.config_object.GetStatus())
      else:
        return json.dumps({})
    else:
      return "This action must be triggered via POST."

  def render_POST(self, request):
    self.SetHeaders(request)
    request.setHeader("Content-Type", "application/json; charset=UTF-8")
    args = request.args.copy()
    if self.action_name in args:
      del args[self.action_name]
    # Convert list of arg values to single value if singly-specified.
    for k, v in args.items():
      if len(v) == 1:
        args[k] = v[0]
      else:
        args[k] = list(v)
    try:
      retval = self.config_object.GetActions()[self.action_name](**args)
      return json.dumps(retval)
    except errors.Error as e:
      import traceback
      traceback.print_exc()
      return json.dumps({"errors": str(e)})
    except (ValueError, TypeError) as e:
      import traceback
      traceback.print_exc()
      return json.dumps({"errors": "invalid parameters: %s" % str(e)})


class ServiceAccountHandler(ConfigObjectHandler):
  isLeaf = True

  def render_POST(self, request):
    self.SetHeaders(request)
    try:
      return self.config_object.GetAuthToken(COMBINED_AUTH_SCOPE).encode("utf-8")
    except:
      return "not available on this platform"


class CameraHandler(ConfigObjectHandler):
  isLeaf = True

  def render_GET(self, request):
    self.SetHeaders(request)
    filename = "capture.jpg"
    self.config_object.Capture(self.config.scratch_directory, filename)
    d = os.path.relpath(self.config.scratch_directory,
                        self.config.base_directory)
    return "<img src='/%s' />" % os.path.join(d, filename)

  def render_POST(self, request):
    katamari_id = request.args.get("katamari_id", None)
    thumbnail_path = request.args.get("thumbnail_path", None)
    acl = request.args.get("acl", "public-read")
    use_previous = request.args.get("use_previous", False)
    preview = request.args.get("preview", False)

    self.SetHeaders(request)
    filename = "capture.jpg"
    if preview:
      filename = "preview.jpg"
      self.config_object.Preview(self.config.scratch_directory, filename)
    elif not use_previous:
      self.config_object.Capture(self.config.scratch_directory, filename)
    path = os.path.join(self.config.scratch_directory, filename)
    with open(path, "rb") as f:
      data = f.read()
    if thumbnail_path and katamari_id:
      ResourceUploader(self.config, katamari_id[0], path, thumbnail_path[0], acl).start()
    return data.encode("base64")


class ResourceUploader(threading.Thread):

  def __init__(self, config, katamari_id, source_path, target_path, acl):
    super(ResourceUploader, self).__init__()
    self.config = config
    self.katamari_id = katamari_id
    self.source_path = source_path
    self.target_path = target_path
    self.acl = acl

  def run(self):
    print "starting uploader"
    for storage in self.config.storage:
      print "Uploading %s to %s" % (self.source_path, storage)
      storage.UploadFile(self.katamari_id, self.source_path, target_path=self.target_path, acl=self.acl)
    print "uploader done"


HANDLERS = {
    camera.FakeCamera: CameraHandler,
    camera.CanonCamera: CameraHandler,
    camera.WebCamera: CameraHandler,
    credential.ServiceAccount: ServiceAccountHandler,
    }
