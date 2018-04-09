#!/bin/bash
# Check if user is root/running with sudo
if [ `whoami` != root ]; then
  echo Please run this script with sudo
  exit
fi

SCRIPT_PATH="$( cd "$( dirname "$0" )" && pwd )"

if [ "`uname -s`" != "Darwin" ]; then
  # Install UDEV rules for USB device
  cp ${SCRIPT_PATH}/51-kinect.rules /etc/udev/rules.d/
  echo "blacklist gspca_kinect" >> /etc/modprobe.d/blacklist.conf
fi

# Run openni setup
cd ${SCRIPT_PATH}/OpenNI-Linux-x64-2.2
source install.sh
cd $ORIG_PATH

