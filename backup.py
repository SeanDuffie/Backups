""" @file backup.py
    @author Sean Duffie
    @brief Functions that are responsible for wrapping the backup and restore functionality.
"""
import logging
import os
# import shutil
import zipfile

import logFormat

### PATH SECTION ###
DEFAULT_PATH = os.path.dirname(__file__)
ACTIVE_PATH = f"{DEFAULT_PATH}/project/"
BACKUP_PATH = f"{DEFAULT_PATH}/backups/"

### LOGGING SECTION ###
logFormat.format_logs(logger_name="BACKUP")
logger = logging.getLogger("BACKUP")

def backup(target_dir: str, zip_filename: str):
    """ Compresses the active directory into a zip archive that can be accessed later.

    Args:
        target_dir (str): Path of directory containing the files to compress
        destination (str): Path of output ZIP archive

    Returns:
        bool: Success?
    """
    # Validity Checks
    assert os.path.isdir(target_dir)
    assert zip_filename.endswith('.zip')

    # Open Zipfile for writing
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        # Iterate over the files in the directory
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)

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
