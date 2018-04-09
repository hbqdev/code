#!/bin/bash
#
# Simple script to install Karnak dependancies

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root (use sudo)" 1>&2
   exit 1
fi

# Pip is installed in /usr/local/bin
PATH=$PATH:/usr/local/bin

# Install Ubuntu packages from list
xargs apt-get install -y <<EOF
make
msgpack-python
libffi-dev
python-dev
python-imaging
python-numpy
python-opencv
python-openssl
python-pip
python-pexpect
python-protobuf
python-scipy
python-serial
python-setuptools
python-yaml
EOF

# Upgrade pip to latest version
pip install -U pip

# Install required python eggs
xargs pip install <<EOF
twisted
autobahn
coverage
google-api-python-client==1.2
gsutil==3.38
mock
nose
primesense
pyinstaller
pypng
pytz
EOF

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}/depth_camera && ./install.sh && cd ${DIR}
