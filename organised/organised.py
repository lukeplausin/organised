#!/usr/bin/env python

import os
import sys
import shutil
import exiftool
import datetime
import filecmp
import logging
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Some hard coded logging stuff so I can see whats happening
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


preferences = {
    "images": {
        "extensions": ["jpg", "jpeg", "png"],
        # "destination": "$HOME/Pictures/Camera/{Date:%Y-%b}/{Date:%Y-%m-%d} ({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"
        "destination": "$HOME/Pictures/Camera/{Date:%Y-%b} ({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"
    },
    "video": {
        "extensions": ["mov", "vid", "xvid"]
    },
    "documents": {
        "extensions": ["doc", "docx", "csv", "txt"]
    }
}

def move_file(source, destination):
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
            os.makedirs(dirname)
        logger.info("Moving from {} to {}".format(source, destination))
        shutil.move(source, destination)

    if not os.listdir(source_dirname):
        logger.info("Removing empty directory {}".format(source_dirname))
        os.rmdir(source_dirname)

def process_images(image_list):
    # Process images

    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(image_list)
    
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
            destination = preferences['images']['destination'].format(
                **file_metadata
            )
            logger.debug(json.dumps(file_metadata, default=str))
            move_file(file_metadata['SourceFile'], destination)
        except KeyError as e:
            logger.error("File {} missing key {}".format(file_metadata['SourceFile'], e))
        except Exception as e:
            logger.error("Exception: {}".format(e))


def main(input_dir='/Users/lukeplausin/Desktop/organise_me/'):
    for root, dirs, files in os.walk(input_dir):
        for name in files:
            # print(os.path.join(root, name))
            for filetype, filetype_data in preferences.items():
                if name.split('.')[-1] in filetype_data['extensions']:
                    # print("Found {} file {}".format(
                    #     filetype, os.path.join(root, name)))
                    file_list = preferences[filetype].get('files', [])
                    file_list.append(os.path.join(root, name))
                    preferences[filetype]['files'] = file_list
        for name in dirs:
            pass
        if all([not os.path.isfile(f) for f in files]) and \
                all([not os.path.isdir(d) for d in dirs]):
            logger.info('Removing empty directory {}'.format(root))
            # os.rmdir(root)
            # print("In directory {}".format(os.path.join(root, name)))
    
    # Process images
    process_images(preferences['images'].get('files', []))


if __name__ == '__main__':
    main()
