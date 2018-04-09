#!/bin/bash
#
# Simple script to install Karnak dependancies for 3D scanners.

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root (use sudo)" 1>&2
   exit 1
fi

# Pip is installed in /usr/local/bin
PATH=$PATH:/usr/local/bin

# Install Ubuntu packages from list
xargs apt-get install -y <<EOF
make
python-pip
python-setuptools
python-yaml
EOF

# Upgrade pip to latest version
pip install -U pip

# Install required python eggs
xargs pip install -U <<EOF
twisted
coverage
google-api-python-client==1.2
gsutil==3.38
mock
nose
EOF
