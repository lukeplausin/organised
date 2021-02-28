from abc import ABC, abstractmethod
import os
import filecmp
import shutil
import click

from . import logger

class BaseOrganizer(ABC):
    def __init__(self, dry_run=False, prompt=True, **config):
        self.file_list = []
        self.dir_list = []
        self.dry_run = dry_run
        self.prompt = prompt
        self.config = config
        self.user_allowed_dirs = []

    @abstractmethod
    def match_file(self, path):
        return False

    @abstractmethod
    def match_dir(self, path):
        return False

    @abstractmethod
    def cleanup_file(self, path):
        pass

    @abstractmethod
    def cleanup_dir(self, path):
        pass

    def process(self):
        for file_judgement in self.file_list:
            self.cleanup_file(file_judgement)

        for dir_judgement in self.dir_list:
            self.cleanup_dir(dir_judgement)

    def _move_file(self, source, destination):
        dirname = os.path.dirname(source)
        if not self.prompt:
            shutil.move(source, destination)
        elif dirname in self.user_allowed_dirs:
            logger.debug(f'User has already allowed directory {dirname}.')
            shutil.move(source, destination)
        else:
            click.secho("Move file from ", nl=False)
            click.secho(source, fg='yellow', nl=False)
            click.secho(" to ", nl=False)
            click.secho(destination, fg='yellow', nl=False)
            click.secho("?")
            response = input("[y: yes|n: no|d: all in directory|a: all] ")
            if response in ['y', 'd', 'a']:
                shutil.move(source, destination)
            else:
                print('skipped..')
            if response == 'd':
                self.user_allowed_dirs.append(dirname)

    def move_file(self, source, destination):
        # Attempt to move a file. Deal with potential issues as they occur.
        destination = os.path.expanduser(os.path.expandvars(destination))
        dirname = os.path.dirname(destination)
        source_dirname = os.path.dirname(source)
        if os.path.isfile(destination):
            # Destination already exists...
            if filecmp.cmp(source, destination):
                logger.info("Deleting file {} duplicated at destination {}".format(
                    source, destination
                ))
                logger.error("TODO")
                # os.remove(source)
            else:
                filename, ext = os.path.splitext(destination)
                ordinal = 1
                comprimise = "{}_{:03d}{}".format(filename, ordinal, ext)
                while os.path.isfile(comprimise):
                    ordinal = ordinal + 1
                    comprimise = "{}_{:03d}{}".format(filename, ordinal, ext)
                logger.info("Renaming file {} to {} due to file clash at {}".format(
                    source, comprimise, destination))
                self._move_file(source, comprimise)
        else:
            # Trivial case. Check destination dir exists
            if not os.path.isdir(dirname):
                logger.info("Creating directory {}".format(dirname))
                if not self.dry_run:
                    os.makedirs(dirname)
            logger.info("Moving from {} to {}".format(source, destination))
            if not self.dry_run:
                self._move_file(source, destination)

        if not os.listdir(source_dirname):
            logger.info("Removing empty directory {}".format(source_dirname))
            if not self.dry_run:
                os.rmdir(source_dirname)
