""" @file backup.py
    @author Sean Duffie
    @brief Functions that are responsible for wrapping the backup and restore functionality.
"""
import datetime
import logging
import os
import zipfile
from tkinter import filedialog

### PATH SECTION ###
DEFAULT_PATH = os.path.dirname(__file__)
ACTIVE_PATH = f"{DEFAULT_PATH}/project/"
BACKUP_PATH = f"{DEFAULT_PATH}/backups/"
if not os.path.isdir(ACTIVE_PATH):
    os.mkdir(ACTIVE_PATH)
if not os.path.isdir(BACKUP_PATH):
    os.mkdir(BACKUP_PATH)

### LOGGING SECTION ###
logger = logging.getLogger("BACKUP")

# def is_changed(path: str):
#     pass

class Pipeline:
    """_summary_

    Returns:
        _type_: _description_
    """
    def __init__(self, src_dir: str = ACTIVE_PATH, zip_dir: str = BACKUP_PATH, name: str = "bak"):
        # Path of directory containing the files to compress
        self.src_dir: str = src_dir
        assert os.path.isdir(self.src_dir)
        # Path of output ZIP archive
        self.zip_dir: str = zip_dir
        assert os.path.isdir(self.zip_dir)
        self.name = name
        if not os.path.exists(os.path.join(zip_dir, name)):
            os.mkdir(os.path.join(zip_dir, name))

    def backup(self, backup_type: str = "Manual"):
        """ Compresses the active directory into a zip archive that can be accessed later.

        Args:
            backup_type (str): How should this backup be classified? (Hourly, Daily, Manual)

        Returns:
            bool: Success?
        """
        assert backup_type in ["Hourly", "Daily", "Manual", "Revert"]

        tstmp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"{self.name}_{tstmp}_{backup_type}.zip"
        os.path.join(self.zip_dir, filename)

        # Validity Checks
        assert os.path.isdir(self.src_dir)

        # Open Zipfile for writing
        with zipfile.ZipFile(self.zip_dir, 'w') as zip_file:
            # Iterate over the files in the directory
            for dirpath, _, filenames in os.walk(self.src_dir):
                for filename in filenames:
                    # Acquire the source path
                    src_path = os.path.join(dirpath, filename)
                    # Determine the output path
                    local_path = src_path.replace(ACTIVE_PATH, "")

                    # Add each file to the ZIP archive
                    zip_file.write(src_path, local_path)

        logger.info("Files compressed into: (%s) from (%s)", self.zip_dir, self.src_dir)

        return True

    def restore(self, zip_name: str):
        """ Restores a zip archive to the working directory.

        Args:
            zip_name (str): Path and filename of the zipfile archive.

        Returns:
            bool: Success?
        """
        # Validity Checks
        print(f"{self.src_dir=}")
        print(f"{self.zip_dir=}")
        # TODO: Replace this with a more automated method
        assert os.path.exists(os.path.join(self.zip_dir, zip_name))

        # Open Zipfile for reading
        with zipfile.ZipFile(self.zip_dir, 'r') as zip_file:
            zip_file.extractall(self.src_dir)

        logger.info("Files extracted from: (%s) to (%s)", self.zip_dir, self.src_dir)

        return True

if __name__ == "__main__":
    # proj = filedialog.askdirectory()
    name = input("What to name the backup?")
    p = Pipeline()
    p.backup(name)
    filedialog.askopenfilename(
        title="Select Zip"
    )
    p.restore(name)
