#!/bin/bash
#
# Create an animated GIF from local images
#
# This script is a tool for debugging 2d image swivels
# captured on a Katamari scan station. It's functionality
# will eventually be replaced by swivel previews in
# the operator UI:  b/9272440 (Live-view swivels)
#
# Note: requres the Graphics Magick package
# sudo apt-get install graphicsmagick
#
# Usage:
# make-local-swivel 20131023-09d3045-sbs7-K-57y1a0gyEzM-2d
#
# Output:
#  An animated GIF titled swivel.GIF will be added to the
# scan directory and thus available via the web interface

scan_id=$1

# Set to 1 for full debugging output, 0 otherwise
_VERBOSE=0
# Where are the scans?
SCAN_ROOT=/scan/katamari/scanning-ops/karnak/static/capture
# Which camera angle (10,20,30)
CAMERA=10
# What to call the resulting scan
OUTPUT_FILENAME=swivel.GIF
# Options to GraphickMagic resizing
OPTIONS="-rotate 180 -quality 98"
# Options to Graphics Magick animation
ANIMATE_OPTIONS="-delay 1"
# Graphics Magick executable for test
GM_TEST_PATH="/usr/bin/gm"

function log () {
    if [[ $_VERBOSE -eq 1 ]]; then
        echo "$@"
    fi
}

if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` scan-id "
  exit
fi


scan_path=${SCAN_ROOT}/${scan_id}

# Is Graphics Magick installed?

if [ ! -e "$GM_TEST_PATH" ]; then
  echo "ERROR: Graphics Magick is not installed"
  echo "sudo apt-get install graphicsmagick"
  exit
fi

# Does the scan exist?
if [ ! -d "$scan_path" ]; then
  echo "ERROR: Unable to find scan_id ${scan_id}"
  exit
fi

echo "Creating swivel for ${scan_id}"

# thumbnail all images into local directory
for angle in {0..355..5}; do
  printf -v padded_angle "%03d" $angle
  orig_image=${scan_path}/${CAMERA}-${padded_angle}.jpg
  thumb_image=./sm-${padded_angle}.jpg
  log "thumbnailing angle ${padded_angle}"
  gm convert ${OPTIONS} -size 640x640 ${orig_image} -resize 640x640 ${thumb_image}
done

# create animated GIF
log "Creating animated GIF"
gm convert ${ANIMATE_OPTIONS} sm-* ${OUTPUT_FILENAME}

# clean up thumbnails
log "Removing thumbnails"
rm *.jpg

# Move animated gif to scan directory
log "Moving animated GIF to scan directory"
mv ${OUTPUT_FILENAME} ${scan_path}

echo "Finishing ${scan_id}"



