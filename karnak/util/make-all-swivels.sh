#!/bin/bash
#
# Generate animated GIFs of all swivels stored on a scanstation
#
# This calls make-local-swivel.sh for each scan stored in the
# capture directory, generating a "swivel.GIF" for each scan
# and storing it in the capture directory.
#
# The CLOBBER variable prevents multiple calls from re-generating
# the same swivels. Set to 1 if swivels should be re-created.

# Where are the scans?
SCAN_ROOT=/scan/katamari/scanning-ops/karnak/static/capture
# What to call the resulting scan
OUTPUT_FILENAME=swivel.GIF
# 1 if want to overwrite existing swivels?
CLOBBER=0


for scan_dir in $(ls ${SCAN_ROOT}); do
  test_file=${SCAN_ROOT}/${scan_dir}/${OUTPUT_FILENAME}
  #echo $test_file
  if [ -e "${test_file}" ]; then
    if [[ $CLOBBER -eq 1 ]]; then
      echo "WARNING: overwriting swivel in ${scan_dir}"
    else
      echo "Skipping existing swivel in ${scan_dir}"
      continue
    fi
  fi
  echo "Creating scan for ${scan_dir}"
  ./make-local-swivel.sh ${scan_dir}
done





