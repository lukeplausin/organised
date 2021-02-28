import os
import shutil
import filecmp

from . import logger


class BaseFile:
    def __init__(self, storage, path):
        self.storage = storage
        self.path = path

    def dirname(self):
        # Return name of "directory" containing file
        dirname = os.path.dirname(self.path)
        return dirname

    def move(self, destination):
        # Move the file from this path to the destination
        shutil.move(self.path, destination)
        self.path = destination

    def is_file(self):
        return os.path.isfile(self.path)

    def is_dir(self):
        return os.path.isdir(self.path)

    def is_duplicate(self, other):
        # Check whether this file is a duplicate with another
        return filecmp.cmp(self.path, other.path)

    def walk(self):
        return self.storage.walk(self.path)

    def delete(self, reason="(none given)"):
        logger.info("Deleting file {}, reason - {}".format(
            self.path, reason
        ))
        os.remove(self.path)
