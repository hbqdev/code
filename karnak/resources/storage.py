# Copyright 2012 Google Inc. All Rights Reserved.

"""Library for pushing assets to storage backend."""
__author__ = "kwc@google.com (Ken Conley)"

import datetime
import os
import re

import boto

from resources import credential
from resources import errors
from resources import katamari
from upload import oauth2_service

GOOGLE_STORAGE = "gs"


def Register(factory):
  factory.RegisterFromDict("BigStore", BigStore.FromDict)


class Storage(katamari.KatamariResource):
  """Base class of storage resources."""

  pass


class BigStore(Storage):

  def __init__(self):
    super(BigStore, self).__init__()
    self._bucket = None

    self._initialized = False

  def Init(self, config):
    # Setup the boto auth_handler plugin.
    credentials = [c for c in config.credentials
                   if isinstance(c, credential.ServiceAccount)]
    if not credentials:
      raise errors.ConfigError("No ServiceAccount credentials for BigStore")
    if len(credentials) > 1:
      raise errors.ConfigError("Multiple ServiceAccount credentials")
    c = credentials[0]
    oauth2_service.ConfigurePlugin(c.service_account_email,
                                   c.private_key_file)
    self._initialized = True

  @staticmethod
  def FromDict(raw_config):
    bs = BigStore()
    bs._bucket = raw_config["bucket"]
    katamari.FromDict(bs, raw_config)
    return bs

  def GetActions(self):
    return dict(fetch=self.Fetch)

  def Fetch(self, uri):
    """Fetches contents of file from BigStore."""
    rewritten = re.sub("katamari-2d-out", "objects3d-scans-sb", uri)
    print "rewrote request to : %s" % rewritten
    file_uri = boto.storage_uri(rewritten, GOOGLE_STORAGE)
    retval = {
      "data": file_uri.get_key().get_contents_as_string().encode("base64")
    }
    return retval

  def UploadFiles(self, unused_kid, files, folder=None):
    """Uploads files to BigStore bucket.

    This API is meant for bulk upload of a set of assets to a target folder.

    Args:
      unused_kid: Katamari ID associated with files.
      files: List of files to upload.
      folder: Override default bucket folder to upload into.  Defaults to
          YYY-MM-DD timestamp.
    Raises:
      errors.IOError: If upload fails.
      errors.InternalError: If not initialized.
    """
    if not self._initialized:
      raise errors.InternalError("Not initialized")
    if not type(files) == list:
      raise errors.InternalError("files must be a list")
    if folder is None:
      folder = datetime.date.today().strftime("%Y-%m-%d")
    for f in files:
      BigStoreUpload(self._bucket, f, os.path.join(folder, os.path.basename(f)),
                     max_retries=5)

  def UploadFile(self, unused_kid, filename, target_path=None, acl=None):
    """Uploads a single file to BigStore bucket.

    This API enables control over the target path of the uploaded asset.

    Args:
      unused_kid: Katamari ID associated with files.
      filename: File to upload.
      target_path: Bucket-relative path of uploaded file.  If not specified,
          defaults to YYYY-MM-DD/<original-filename>.
    Raises:
      errors.IOError: If upload fails.
      errors.InternalError: If not initialized.
    """
    if not self._initialized:
      raise errors.InternalError("Not initialized")
    if target_path is None:
      target_folder = datetime.date.today().strftime("%Y-%m-%d")
      target_path = os.path.join(target_folder, os.path.basename(filename))
    # TODO(jarussell): Move max_retries to constant or config file.
    BigStoreUpload(self._bucket, filename, target_path, acl=acl, max_retries=5)


def BigStoreUpload(bucket_id, filename, target_filename, acl=None,
                   max_retries=0):
  """
  Args:
    bucket_id: BigStore bucket ID.
    filename: File to upload.
    target_path: Bucket-relative path of uploaded file.  Defaults to the name of
        the source file.
    acl: Optional Boto ACL to assign to object, e.g., 'public-read'.
    max_retries: Maximum number of attempts before giving up.
  Raises:
    errors.IOError: If upload fails.
  """
  uri_val = "%s/%s" % (bucket_id, target_filename)
  print "uploading to GS URI", uri_val, "acl", acl
  file_uri = boto.storage_uri(uri_val, GOOGLE_STORAGE)
  num_attempts = 0
  key = file_uri.new_key()
  while True:
    num_attempts += 1
    if acl:
      key.set_contents_from_file(open(filename, "r"), policy=acl)
    else:
      key.set_contents_from_file(open(filename, "r"))
    num_bytes = key.size
    expected = os.path.getsize(filename)
    if num_bytes != expected:
      print ("BigStore: upload size mismatch: %s vs %s (expected)" %
             (num_bytes, expected))
      if num_attempts <= max_retries:
        print "Re-attempting upload...%d of %d" % (num_attempts, max_retries)
        continue
      else:
        raise errors.IOError("Could not upload to BigStore after %d attempts" %
                             num_attempts)
    else:
      break
