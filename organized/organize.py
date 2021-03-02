#!/usr/bin/env python

import os
import sys
import datetime
import logging
import logging.config
import json
import re
import yaml
import pkg_resources

from .storage import get_storage
from .storage.base_file import BaseFile
from .helpers import GitOrganizer, CameraOrganizer, JunkOrganizer

from . import DEFAULTS
from . import logger


ORGANIZER_NAMES = ['camera', 'git', 'junk']

def load_organizers(organizers=ORGANIZER_NAMES, **kwargs):
    org_objects = []
    for organizer in organizers:
        if organizer == 'camera':
            org_objects.append(CameraOrganizer(**kwargs))
        elif organizer == 'git':
            org_objects.append(GitOrganizer(**kwargs))
        elif organizer == 'junk':
            org_objects.append(JunkOrganizer(**kwargs))
        else:
            msg = "Unknown organizer {}".format(organizer)
            logger.critical(msg)
            raise ValueError(msg)
    return org_objects


def main(input_dir, **kwargs):
    organizers = load_organizers(**kwargs)
    logger.info("Step 1, scanning input directory")

    source = get_storage(input_dir, **kwargs)
    for root, dirs, files in source.walk():
        for file in files:
            file_type_recognised = []
            for organizer in organizers:
                if isinstance(file, BaseFile):
                    file_obj = file
                else:
                    file_obj = source.storage.join(root, file, as_object=True)
                if organizer.match_file(file_obj):
                    # The organizer recognises this file type
                    file_type_recognised.append(organizer.__class__)
            if file_type_recognised:
                logger.debug("File {} matched {} organizers".format(
                    file_obj.path, file_type_recognised))
            else:
                pass
                # logger.debug("File {} matched no organizers".format(full_filename))

        for dirname in dirs:
            dir_type_recognised = []
            for organizer in organizers:
                full_dirname = source.storage.join(root, dirname)
                if organizer.match_dir(full_dirname):
                    dir_type_recognised.append(organizer.__class__)
                # logger.debug("Directory {} matched no organizers".format(full_dirname))

    logger.info("Step 2, clean up phase")
    for organizer in organizers:
        organizer.process()


# def cli():
#     try:
#         import argparse 
#     except ImportError:
#         print("ERROR: You are running Python < 2.7. Please use pip to install argparse:   pip install argparse")

#     parser = argparse.ArgumentParser(add_help=True, description="Organize documents based on tags and metadata, to help keep your digital life tidy.")
#     parser.add_argument("--input-dir", "-i", type=str, help="Path to input directory (files to sort)", default='~/Desktop/organize_me/')
#     parser.add_argument("--config-dir", "-c", type=str, help="Path to config directory", default='~/.organized/')
#     parser.add_argument("--dry-run", help="Whether to dry run the organizer. If set, the organizer won't do anything.", action='store_true')

#     args = parser.parse_args()

#     # Load config from file
#     if args.config_dir:
#         config_dir = args.config_dir
#     else:
#         config_dir = DEFAULTS['config_dir']
#     config_dir = os.path.expanduser(os.path.expandvars(config_dir))
#     config_file = os.path.join(config_dir, "config.yaml")
#     if os.path.exists(config_file):
#         logger.info('opening file config {}'.format(config_file))
#         with open(config_file, 'r') as f:
#             file_config = yaml.safe_load(f)
#     else:
#         logger.info('Creating default config file at {}'.format(config_file))
#         if not os.path.isdir(config_dir):
#             os.mkdir(config_dir)
#         with open(config_file, 'w') as f:
#             default_config = yaml.dump(DEFAULTS, default_flow_style=False)
#             f.write(default_config)
#             logger.debug(default_config)
#         file_config = {}

#     logging_config_file = os.path.join(config_dir, 'logger.yaml')
#     if not os.path.exists(logging_config_file):
#         # logger.info('Creating default logging file at {}'.format(config_file))
#         pass
#     if os.path.exists(logging_config_file):
#         logger.info('Loading logger configuration file at {}'.format(logging_config_file))
#         with open(logging_config_file, 'r') as f:
#             logging.config.dictConfig(yaml.safe_load(f))

#     # TODO copy default config over from directory


#     # Resolve config from different sources
#     config = DEFAULTS
#     if file_config:
#         config.update(file_config)
#     config.update(args.__dict__)
#     config['config_dir'] = config_dir

#     main(**config)
