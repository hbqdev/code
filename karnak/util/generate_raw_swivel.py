"""Generate a swivel of the front camera using ffmpeg.

This module can be used as a template module for generating a
raw swivel at the end of a scan.  It can be called using:

import generate_raw_swivel

generate_raw_swivel.CreateRawSwivelFile(camera_num,
                                        capture_dir,
                                        katamari_id)

where camera_num = 10, 20, 30 (front, ortho, or top)
      capture_dir = ~katamari/scanning-ops/karnak/static/capture
      katamari_id = scan_id
"""

import os
import shutil
import subprocess

# The interval between camera angle shots
ANGLE_INTERVAL = 5
# The temporary sequential image filename
IMAGE_FILENAME = "image"

# The following variables are global lists
# because they are going to be joined into
# one larger array for the Python subprocess module
# to call
FFMPEG_CMD = ["ffmpeg"]
LOOP_OPTION = ["-loop", "1"]
IMAGE_OPTION = ["-f", "image2"]
FRAMERATE_OPTION = ["-r", "20"]
INPUT_OPTION = ["-i", "image%02d.jpg"]
TIME_OPTION = ["-t", "20"]
OUTPUT_OPTION = ["swivel.avi"]


class Error(Exception):
  """Base error class."""
  pass


class SwivelError(Error):
  """Swivel Error."""
  pass


def CreateRawSwivelFile(camera_number, capture_directory, katamari_id):
  """Launches swivel generation process.

  Args:
    camera_number: the id associated with the camera
    capture_directory: The directory where raw images are stored.
    katamari_id: The scan id of a raw scan
  """
  image_path = os.path.join(capture_directory, katamari_id)

  count = GenerateSequentialImageFiles(camera_number, image_path)
  GenerateRawSwivel(image_path)
  RemoveSequentialImagesFiles(image_path, count)


def RemoveSequentialImagesFiles(image_path, image_count):
  """Delete the sequential image files.

  Args:
    image_path: Path to the raw scan id
    image_count: The number of images to delete
  """
  for count in range(0, image_count):
    image_name = "%s%02d.jpg" % (IMAGE_FILENAME, count)
    os.remove(os.path.join(image_path, image_name))


def GenerateSequentialImageFiles(camera_number, image_path):
  """Generate the sequential image filenames.

  FFMPEG requires the images to be sequentially named in order
  to stitch them together to form an animated shot.

  Args:
    camera_number: The id associated with a camera
    image_path: Path to the raw scan id

  Returns:
    The number of image files.
  """
  image_count = 0

  for angle in range(0, 360, ANGLE_INTERVAL):
    # Use the generated thumbnail images
    original_image_name = "%s-%03d.tn.jpg" % (camera_number, angle)
    # Copy the thumbnail files as "image01, image02 ... imagexx".
    new_image_name = "%s%02d.jpg" % (IMAGE_FILENAME, image_count)
    # Keep track of the number of copied files for later removal
    image_count += 1

    shutil.copyfile(os.path.join(image_path, original_image_name),
                    os.path.join(image_path, new_image_name))

  return image_count


def GenerateRawSwivel(image_path):
  """Generate the swivel animation.

  Args:
    image_path: Path to the raw scan id
  """
  # Join together the various FFMPEG commands and options
  generate_swivel_cmd = (FFMPEG_CMD + LOOP_OPTION + IMAGE_OPTION +
                         FRAMERATE_OPTION + INPUT_OPTION +
                         TIME_OPTION + OUTPUT_OPTION)

  try:
    subprocess.check_call(generate_swivel_cmd, cwd=image_path,
                          stderr=subprocess.PIPE)
  except subprocess.CalledProcessError as swivel_error:
    raise SwivelError("Swivel failed to generate: %s", swivel_error)
