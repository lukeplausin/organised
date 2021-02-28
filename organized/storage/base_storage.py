# Base storage class
import os
from . import logger

from .base_file import BaseFile

class BaseStorage:

    def __init__(self, **config):
        pass

    def is_file(self, path):
        return os.path.isfile(path)

    def is_dir(self, path):
        return os.path.isdir(path)

    def mkdir(self, path):
        logger.info("Creating directory {}".format(path))
        return os.makedirs(path)

    def list_dir(self, path):
        return os.listdir(path)

    def rmdir(self, path):
        logger.info("Removing empty directory {}".format(path))
        return os.rmdir(path)

    def walk(self, path):
        # Iterate over files and folders
        return os.walk(path)

    def join(self, base, path, as_object=False):
        # Join two file paths
        new_path = os.path.join(base, path)
        if as_object:
            return self.file(new_path)
        else:
            return new_path

    def file(self, path):
        # Return a new file object from the given path
        return BaseFile(storage=self, path=path)
