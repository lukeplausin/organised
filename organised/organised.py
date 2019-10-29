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


from .git_organiser import GitOrganiser
from .camera_organiser import CameraOrganiser
from .junkfile_organiser import JunkOrganiser

from . import DEFAULTS

logger = logging.getLogger(__name__)

# Some hard coded logging stuff so I can see whats happening
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# def process_junk(input_file_list):
#     for file in input_file_list:
#         logger.info("Removing junk file {}".format(file))
#         # os.remove(file)


# def cleanup_empty_dirs(input_dir):
#     # Remove empty directories in a tree
#     # for root, dirs, files in os.walk(input_dir):
#     #     if all([not os.path.isfile(f) for f in files]) and \
#     #             all([not os.path.isdir(d) for d in dirs]):
#     #         logger.info('Removing empty directory {}'.format(root))
#     #         os.rmdir(root)
#     pass



def load_organisers(config):
    org_objects = []
    for organiser in config['preferences']['organisers']:
        if organiser == 'camera':
            org_objects.append(CameraOrganiser(config))
        elif organiser == 'git':
            org_objects.append(GitOrganiser(config))
        elif organiser == 'junk':
            org_objects.append(JunkOrganiser(config))
        else:
            msg = "Unknown organiser {}".format(organiser)
            logger.critical(msg)
            raise ValueError(msg)
    return org_objects


def main(input_dir, preferences, **kwargs):
    config = kwargs
    config['preferences'] = preferences
    organisers = load_organisers(config)

    logger.info("Step 1, scanning input directory")
    input_dir = os.path.expanduser(os.path.expandvars(input_dir))
    for root, dirs, files in os.walk(input_dir):
        # logger.debug("Scanning in {}".format(root))
        for name in files:
            file_type_recognised = []
            for organiser in organisers:
                full_filename = os.path.join(root, name)
                if organiser.match_file(full_filename):
                    # The organiser recognises this file type
                    file_type_recognised.append(organiser.__class__)
            if file_type_recognised:
                logger.debug("File {} matched {} organisers".format(full_filename, file_type_recognised))
            else:
                pass
                # logger.debug("File {} matched no organisers".format(full_filename))

        for dirname in dirs:
            dir_type_recognised = []
            for organiser in organisers:
                full_dirname = os.path.join(root, dirname)
                if organiser.match_dir(full_dirname):
                    dir_type_recognised.append(organiser.__class__)
                # logger.debug("Directory {} matched no organisers".format(full_dirname))

    logger.info("Step 2, clean up phase")
    for organiser in organisers:
        organiser.process()


def cli():
    try:
        import argparse 
    except ImportError:
        print("ERROR: You are running Python < 2.7. Please use pip to install argparse:   pip install argparse")

    parser = argparse.ArgumentParser(add_help=True, description="Organise documents based on tags and metadata, to help keep your digital life tidy.")
    parser.add_argument("--input-dir", "-i", type=str, help="Path to input directory (files to sort)", default='~/Desktop/organise_me/')
    parser.add_argument("--config-dir", "-c", type=str, help="Path to config directory", default='~/.organised/')
    parser.add_argument("--dry-run", help="Whether to dry run the organiser. If set, the organiser won't do anything.", action='store_true')

    args = parser.parse_args()

    # Load config from file
    if args.config_dir:
        config_dir = args.config_dir
    else:
        config_dir = DEFAULTS['config_dir']
    config_dir = os.path.expanduser(os.path.expandvars(config_dir))
    config_file = os.path.join(config_dir, "config.yaml")
    if os.path.exists(config_file):
        logger.info('opening file config {}'.format(config_file))
        with open(config_file, 'r') as f:
            file_config = yaml.safe_load(f)
    else:
        logger.info('Creating default config file at {}'.format(config_file))
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
        with open(config_file, 'w') as f:
            default_config = yaml.dump(DEFAULTS, default_flow_style=False)
            f.write(default_config)
            logger.debug(default_config)
        file_config = {}

    logging_config_file = os.path.join(config_dir, 'logger.yaml')
    if not os.path.exists(logging_config_file):
        # logger.info('Creating default logging file at {}'.format(config_file))
        pass
    if os.path.exists(logging_config_file):
        logger.info('Loading logger configuration file at {}'.format(logging_config_file))
        with open(logging_config_file, 'r') as f:
            logging.config.dictConfig(yaml.safe_load(f))

    # TODO copy default config over from directory


    # Resolve config from different sources
    config = DEFAULTS
    if file_config:
        config.update(file_config)
    config.update(args.__dict__)
    config['config_dir'] = config_dir

    main(**config)
