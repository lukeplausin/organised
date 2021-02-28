# For organising nuisance files

import os
import shutil
import subprocess
import logging
import json
import datetime
import exiftool


logger = logging.getLogger(__name__)


from . import BaseOrganizer


JUNK_FILENAMES = ['.DS_Store']
JUNK_EXTENSIONS = ['.tmp']


class JunkOrganizer(BaseOrganizer):
    def __init__(
                self, cleanup_empty_dirs=True, 
                file_extensions=JUNK_EXTENSIONS,
                file_names=JUNK_FILENAMES,
                **config):
        super().__init__(**config)
        self.config = config
        self.dry_run = config['dry_run']
        self.file_list = []
        self.dir_list = []
        self.file_extensions = file_extensions
        self.file_names = file_names
        self.cleanup_empty_dirs = cleanup_empty_dirs

        # if "org.junk" in self.config["preferences"].keys():
        #     # Check for overrides in config
        #     plugin_config = self.config["preferences"]["org.junk"]
        #     if "file_extensions" in plugin_config.keys():
        #         self.file_extensions = plugin_config["file_extensions"]
        #     if "file_extensions" in plugin_config.keys():
        #         self.file_extensions = plugin_config["file_extensions"]
        #     if "destination" in plugin_config.keys():
        #         self.destination = plugin_config["destination"]


    def match_file(self, path):
        path_noext, ext = os.path.splitext(path)
        if ext in self.file_extensions:
            judgement = (path, "File has known {} extension".format(ext))
            self.file_list.append(judgement)
            logger.info("{} match - {}".format(*judgement))
            return True
        elif os.path.basename(path) in self.file_names:
            judgement = (path, "Known junk file".format(ext))
            self.file_list.append(judgement)
            logger.info("{} match - {}".format(*judgement))
            return True
        else:
            return False


    def match_dir(self, path):
        if self.cleanup_empty_dirs and len(os.listdir(path) ) == 0:
            judgement = (path, "Directory is empty")
            self.dir_list.append(judgement)
            logger.info("{} match - {}".format(*judgement))
            return True
        else:
            return False

    def cleanup_dir(self, judgement):
        # TODO use the base class method..
        if self.dry_run:
            logger.info('DRYRUN: Removing directory {}'.format(judgement[0]))
        else:
            logger.info('Removing directory {}'.format(judgement[0]))
            os.rmdir(judgement[0])

    
    def cleanup_file(self, judgement):
        if self.dry_run:
            logger.info('DRYRUN: Removing file {}'.format(judgement[0]))
        else:
            logger.info('Removing file {}'.format(judgement[0]))
            os.remove(judgement[0])
