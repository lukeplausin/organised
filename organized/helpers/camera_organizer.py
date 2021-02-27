import os
import shutil
import subprocess
import logging
import json
import datetime
import exiftool

from .base_organizer import BaseOrganizer
from . import logger


class CameraOrganizer(BaseOrganizer):
    def __init__(self, config):
        super().__init__(config)
        self.file_extensions = [".jpg", ".jpeg", ".png", ".3gp", ".mov", ".mp4"]
        self.destination = "~/Pictures/MyPhotos/{Date:%Y-%m}_({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"

        if "org.camera" in self.config["preferences"].keys():
            # Check for overrides in config
            plugin_config = self.config["preferences"]["org.camera"]
            if "file_extensions" in plugin_config.keys():
                self.file_extensions = plugin_config["file_extensions"]
            if "destination" in plugin_config.keys():
                self.destination = plugin_config["destination"]

    def match_file(self, path):
        path_noext, ext = os.path.splitext(path)
        if ext in self.file_extensions:
            judgement = (path, "File has known {} extension".format(ext))
            self.file_list.append(judgement)
            logger.debug("{} match - {}".format(*judgement))
            return True
        else:
            return False
        # else:
        #     for pattern in spec.get('patterns', []):
        #         if re.match(pattern, name):
        #             return True

    def match_dir(self, path):
        return False

    def cleanup_dir(self, judgement):
        pass
    
    def cleanup_file(self, judgement):
        destination = self.config['preferences']['org.camera']['destination'].format(
            **judgement
        )
        if (self.config.get('dry_run', True)):
            print("DRYRUN: Move file {} to {}".format(
                judgement['SourceFile'], destination))
        else:
            # move_file(file_metadata['SourceFile'], destination)
            self.move_file(judgement['SourceFile'], destination)

    def process(self):
        # Process images with exif metadata
        with exiftool.ExifTool() as et:
            file_list = [file_item[0] for file_item in self.file_list]
            if file_list:
                metadata = et.get_metadata_batch(file_list)
            else:
                metadata = []
        
        for file_metadata in metadata:
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

                # metadata['Augmented:CreateDate'] = date
                self.cleanup_file(file_metadata)
                
            except KeyError as e:
                logger.error("File {} missing key {}".format(file_metadata['SourceFile'], e))
                logger.debug(json.dumps(file_metadata, default=str, indent=2))
            except Exception as e:
                logger.error("Exception: {}".format(e))
