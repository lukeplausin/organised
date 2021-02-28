import os
import shutil
import subprocess
import logging
import json
import datetime
import exiftool

from .base_organizer import BaseOrganizer
from . import logger
from ..storage import get_storage
from ..logic.action import Action

DEFAULT_EXTENSIONS = [".jpg", ".jpeg", ".png", ".3gp", ".mov", ".mp4"]
DEFAULT_BASE_PATH = '~/Pictures/Camera'
DEFAULT_FILE_PATH = "{Date:%Y-%m} ({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"


class CameraOrganizer(BaseOrganizer):
    def __init__(
            self,
            base_path=DEFAULT_BASE_PATH,
            file_path=DEFAULT_FILE_PATH,
            **config
            ):
        super().__init__(**config)
        self.file_extensions = DEFAULT_EXTENSIONS
        self.destination = os.path.join(base_path, file_path)

        # TODO - clean up config management
        if "org_camera_file_extensions" in config.keys():
            self.file_extensions = config["org_camera_file_extensions"]
        if "org_camera_destination" in config.keys():
            self.destination = config["org_camera_destination"]

    def match_file(self, file_obj):
        path_noext, ext = os.path.splitext(file_obj.path)
        if ext in self.file_extensions:
            action = Action(
                source=file_obj,
                reason="File has known {} extension".format(ext),
            )
            self.file_list.append(action)
            return True
        else:
            return False

    def match_dir(self, path):
        return False

    def cleanup_dir(self, action):
        pass
    
    def cleanup_file(self, action):
        destination_name = self.destination.format(
            **action.file_metadata
        )
        destination = get_storage(destination_name)
        action.destination = destination
        self.move_file(action.source, destination)

    def process(self):
        # Process images with exif metadata
        with exiftool.ExifTool() as et:
            file_list = [file_item.source.path for file_item in self.file_list]
            if file_list:
                metadata = et.get_metadata_batch(file_list)
            else:
                metadata = []
        
        for idx, file_metadata in enumerate(metadata):
            try:
                # Augment the data
                file_metadata = {
                    k.replace(":", "_"): v for k, v in file_metadata.items()
                }
                file_metadata['File_FileTypeExtension'] = file_metadata['File_FileTypeExtension'].lower()
                if 'EXIF_CreateDate' in file_metadata.keys():
                    date = file_metadata['EXIF_CreateDate']
                else:
                    date = file_metadata['File_FileModifyDate']
                file_metadata['Augmented_CreateDate'] = date
                if '+' in date:
                    date_parsed = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S%z')
                else:
                    date_parsed = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
                file_metadata['Date'] = date_parsed
                action = self.file_list[idx]
                action.file_metadata = file_metadata

                # metadata['Augmented:CreateDate'] = date
                self.cleanup_file(action)
                
            except KeyError as e:
                logger.info("File {} missing key {}".format(file_metadata['SourceFile'], e))
                logger.debug(json.dumps(file_metadata, default=str, indent=2))
            except Exception as e:
                logger.exception(e)
