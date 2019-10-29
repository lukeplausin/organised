from abc import ABC, abstractmethod
import os
import filecmp
import shutil
import logging


logger = logging.getLogger(__name__)


DEFAULTS={
    # "input_dir": "~/desktop/"
    "config_dir": "~/.organised/",

    "preferences": {
        "organisers": ["camera", "git", "junk"],
        "org.camera": {
            "file_extensions": [".jpg", ".jpeg", ".png", ".3gp", ".mov", ".mp4"],
            # "destination": "$HOME/Pictures/Camera/{Date:%Y-%b}/{Date:%Y-%m-%d} ({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"
            "destination": "~/Pictures/MyPhotos/{Date:%Y-%m}_({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"
        },
        "org.junk": {
            "file_extensions": [".tmp"],
            "remove_patterns": [".DS_Store"]
        },
        # "movie": {
        #     "extensions": ["mov", "vid", "xvid"]
        # },
        "documents": {
            "extensions": ["doc", "docx", "csv", "txt"]
        }
    }
}

class BaseOrganiser(ABC):
    def __init__(self, config={}):
        self.file_list = []
        self.dir_list = []
        self.config = config
        self.dry_run = config.get('dry_run', False)

    
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
                print("TODO")
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
                shutil.move(source, comprimise)
        else:
            # Trivial case. Check destination dir exists
            if not os.path.isdir(dirname):
                logger.info("Creating directory {}".format(dirname))
                if not self.dry_run:
                    os.makedirs(dirname)
            logger.info("Moving from {} to {}".format(source, destination))
            if not self.dry_run:
                shutil.move(source, destination)

        if not os.listdir(source_dirname):
            logger.info("Removing empty directory {}".format(source_dirname))
            if not self.dry_run:
                os.rmdir(source_dirname)
