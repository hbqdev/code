#!/bin/bash
#
# Helper script to start operations on a scanstation
# TODO: merge into the Makefile like everything else
#
HOSTNAME=`hostname`
ROOT=/scan/katamari/scanning-ops/karnak
. ${ROOT}/depth_camera/setup.sh
export PYTHONPATH=${ROOT}
# start_camera_server is created by make sanity
bash util/start_camera_server.sh
python ui/websocket.py config/${HOSTNAME}.yaml &
