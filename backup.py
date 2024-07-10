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
logname = ACTIVE_PATH + '/' + 'MCSERVER.log'
logFormat.format_logs(logger_name="MCLOG", file_name=logname)
logger = logging.getLogger("MCLOG")
logger.info("Logname: %s", logname)

def backup():
    # Directory containing the files to compress
    directory = '/path/to/directory'

    # Name of the output ZIP archive
    zip_filename = 'archive.zip'

    # Create a new ZIP archive
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        # Iterate over the files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Add each file to the ZIP archive
            zip_file.write(file_path, filename)

    logger.info(f"Files compressed into: %s", zip_filename)

    return True
