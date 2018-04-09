#!/usr/bin/python

"""Create camera_server config files from station YAML.

This creates station-specific camera_server config files based
on the standard station YAMLs. Karnak will eventually have
hooks into the camera server, at which point this global
configuration will no longer be needed.

Args:
  Requires path to the station-specific YAML
  Optional path to the artproject camera server

Example Usage:
./configure_camera_server.py ../config/sbs11.yaml

Josh Weaver <jweaver@google.com>
"""

import argparse
import json
import logging
import os
import sys
import yaml

TEMPLATE_FILENAME = 'artproject_config_template.json'
EXPORT_FILENAME = 'artproject_config.json'
EXPORT_TOP_FILENAME = 'artproject_config_top.json'

KARNAK_ROOT = '/scan/katamari/scanning-ops/karnak'

SUPPORTED_CAMERAS = ['front_camera', 'top_camera', 'ortho_camera']

# ISOs supported by ArtProject camera
VALID_ISO = [
    100, 125, 160, 200, 250, 320, 400, 500, 640, 800,
    1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000, 6400, 8000,
    10000, 12800, 20000, 25600
    ]

# Exposure values supported by ArtProject camera
VALID_EXP = [
    '1/250', '1/200', '1/160', '1/125', '1/100', '1/80', '1/60',
    '1/50', '1/40', '1/30', '1/25', '1/20', '1/15', '1/13',
    '1/10', '1/8', '1/6', '1/5', '1/4'
    ]

# Apertures supported by ArtProject camera
VALID_APERTURE = [2, 2.8, 4, 5.6, 8, 11, 13, 16, 18, 22, 32, 36]


def LoadStationConfig(yaml_file):
  """Load station YAML."""
  station_yaml = open(yaml_file)
  return yaml.load(station_yaml)


def ExtractCameraValues(yaml_buffer):
  """Extract needed camera values from station YAML."""
  config = {}
  for resource in yaml_buffer['resources']:
    if resource['name'] in SUPPORTED_CAMERAS:
      camera = {}
      camera['iso'] = resource['iso']
      camera['exp'] = resource['shutterspeed']
      camera['aperture'] = resource['aperture']
      config[resource['name']] = camera
  return config


def VerifyStationConfig(camera_config):
  """Ensure camera settings are valid.

  Args:
    camera_config: dictionary of camera to value mappings

  Returns:
    True if camera_config has valid parameters
  """
  cameras = camera_config.keys()
  if 'top_camera' not in cameras:
    logging.warn('Missing Top camera!')

  if (('front_camera' not in cameras) and
      ('ortho_camera' not in cameras)):
    logging.error('Ortho or Front must be defined')
    return False

  for camera in camera_config.values():
    if camera['exp'] not in VALID_EXP:
      logging.error('%s is invalid exposure', camera['exp'])
      return False

    if camera['iso'] not in VALID_ISO:
      logging.error('%s is invalid iso', camera['iso'])
      return False

    if camera['aperture'] not in VALID_APERTURE:
      logging.error('%s is invalid aperture', camera['aperture'])
      return False

  return True


def LoadArtprojectTemplate(template_file):
  """Import template JSON."""
  return json.load(open(template_file))


def FormatAperture(f_num):
  """Format aperture for ArtProject: F5_6, F11, etc."""
  if f_num >= 10:
    return 'F%d' % (f_num)
  else:
    base = int(f_num)
    fract = f_num * 10 % 10
    return 'F%d_%d' % (base, fract)


def ExpandTemplate(template, camera, include_aperture=False):
  """Helper function to fill in template values."""
  template['camera_and_setting'][1]['settings']['iso'] = \
      'ISO_%s' % (camera['iso'])
  template['camera_and_setting'][1]['settings']['exposure'] = \
      'E%s' % (camera['exp'].replace('/', '_'))
  if include_aperture:
    template['camera_and_setting'][1]['settings']['aperture'] = \
        FormatAperture(camera['aperture'])
  else:
    template['camera_and_setting'][1]['settings'].pop('aperture', None)
  return template


def ExportArtprojectConfigs(camera_config, template_buffer, output_path):
  """Create regular and top configs for this station.

  Args:
    camera_config: dict of camera values created by ExtractCameraValues
    template_buffer: JSON template from LoadArtprojectTemplate
    output_path: directory to write config files
  """
  # Top camera (optional for floor rig)
  if 'top_camera' in camera_config.keys():
    top_json = ExpandTemplate(template_buffer,
                              camera_config['top_camera'],
                              include_aperture=True)
    with open(output_path + EXPORT_TOP_FILENAME, 'w') as f:
      json.dump(top_json, f, ensure_ascii=False, indent=2)

  # Other camera
  if 'front_camera' in camera_config.keys():
    camera = 'front_camera'
  else:
    camera = 'ortho_camera'
  front_json = ExpandTemplate(template_buffer, camera_config[camera])
  with open(output_path + EXPORT_FILENAME, 'w') as f:
    json.dump(front_json, f, ensure_ascii=False, indent=2)


def CreateArgParser():
  parser = argparse.ArgumentParser(
      description='Create artproject camera config files.')
  parser.add_argument('station_cfg', type=str,
                      help='station specific yaml file')
  parser.add_argument('--artproject_path', type=str,
                      default=KARNAK_ROOT + '/camera_server/',
                      help='artproject camera path')
  return parser


def main():
  parser = CreateArgParser()
  args = parser.parse_args()

  yaml_buffer = LoadStationConfig(args.station_cfg)
  camera_cfg = ExtractCameraValues(yaml_buffer)
  if not VerifyStationConfig(camera_cfg):
    logging.error('Invalid yaml %s', args.station_cfg)
    sys.exit(1)

  template_file = args.artproject_path + TEMPLATE_FILENAME
  template_buffer = LoadArtprojectTemplate(template_file)

  ExportArtprojectConfigs(camera_cfg,
                          template_buffer,
                          args.artproject_path)


if __name__ == '__main__':
  main()
