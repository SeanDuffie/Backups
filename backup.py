""" @file backup.py
    @author Sean Duffie
    @brief Functions that are responsible for wrapping the backup and restore functionality.
"""
import logging
import os
# import shutil
import zipfile
from tkinter import filedialog

import logFormat

### PATH SECTION ###
DEFAULT_PATH = os.path.dirname(__file__)
ACTIVE_PATH = f"{DEFAULT_PATH}/project/"
BACKUP_PATH = f"{DEFAULT_PATH}/backups/"

### LOGGING SECTION ###
logFormat.format_logs(logger_name="BACKUP")
logger = logging.getLogger("BACKUP")

# def is_changed(path: str):
    
#     pass

def backup(zip_filename: str, target_dir: str = None, zip_path: str = None):
    """ Compresses the active directory into a zip archive that can be accessed later.

    Args:
        target_dir (str): Path of directory containing the files to compress
        destination (str): Path of output ZIP archive

    Returns:
        bool: Success?
    """
    if target_dir is None:
        target_dir = ACTIVE_PATH
    if zip_path is None:
        zip_path = f"{BACKUP_PATH}/{zip_filename}.zip"

    # Validity Checks
    assert os.path.isdir(target_dir)

    # Open Zipfile for writing
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        # Iterate over the files in the directory
        for dirpath, dirnames, filenames in os.listdir(target_dir):
            for filename in filenames:
                # print(dirpath, dirnames, filename)
                local_path = os.path.join(dirpath, filename).replace(zip_path, "")

                # TODO: Fix local directory in zip
                file_path = os.path.join(target_dir, local_path)

                # Add each file to the ZIP archive
                zip_file.write(file_path, filename)

    logger.info(f"Files compressed into: %s", zip_filename)

    return True

def restore(zip_filename: str, target_dir: str):
    """ Restores a zip archive to the working directory.

    Args:
        zip_filename (str): Path and filename of the zipfile archive.
        target_dir (str): Path where the zip file will be extracted to.

    Returns:
        bool: Success?
    """
    # Validity Checks
    assert os.path.isdir(target_dir)
    assert zip_filename.endswith('.zip')

    # Open Zipfile for reading
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        zip_file.extractall(target_dir)

    logger.info("Files extracted from: %s", zip_filename)

    return True

if __name__ == "__main__":
    # proj = filedialog.askdirectory()
    name = input("What to name the backup?")
    backup(name)
