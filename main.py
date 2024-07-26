""" @file main.py
    @author Sean Duffie
    @brief 
"""
import logging
import os
from tkinter import filedialog

import logFormat
from backup import Pipeline
from schedule import Scheduler

### PATH SECTION ###
DEFAULT_PATH = os.path.dirname(__file__)
ACTIVE_PATH = os.path.join(DEFAULT_PATH, "project")
BACKUP_PATH = os.path.join(DEFAULT_PATH, "backups")
if not os.path.isdir(ACTIVE_PATH):
    os.mkdir(ACTIVE_PATH)
if not os.path.isdir(BACKUP_PATH):
    os.mkdir(BACKUP_PATH)

### LOGGING SECTION ###
logFormat.format_logs(logger_name="BACKUP")
logger = logging.getLogger("BACKUP")

def launch(proj_name: str = "Project", src_dir: str = "", interval: int = 1800):
    """ Launches the Scheduler process and attaches the Backup Pipeline

    Args:
        proj_name (str, optional): Name of the Project (subjective). Defaults to "Project".
        src_dir (str, optional): Directory to take backups from. Defaults to "".
        interval (int, optional): How often to backup in seconds. Defaults to 1800.

    Returns:
        Pipeline: The objectified backup class
        Scheduler: The wrapper for the schedule process
    """
    if src_dir == "":
        logger.warning("No source directory detected! Using default:")
        logger.warning(ACTIVE_PATH)
        src_dir = ACTIVE_PATH

    logger.info("Configuring Backup: Every %d minutes from %s", interval/60, src_dir)
    pipeline = Pipeline(src_dir=src_dir, project_name=proj_name)
    tmr = Scheduler(interval, pipeline.backup, args=["Hourly"])
    tmr.start()
    return pipeline, tmr

def kill(tmr: Scheduler):
    """ Kills the Scheduler politely.

    Args:
        tmr (Scheduler): The object container for the Scheduler process
    """
    tmr.cancel()

if __name__ == "__main__":
    NAME = input("Project Name: ")
    SRC_DIR = filedialog.askdirectory(
        title="Select Source Directory",
        initialdir=f"{DEFAULT_PATH}/"
    )
    INTERVAL = int(input("Minutes between backups: ")) * 60
    P, TMR = launch(proj_name=NAME, src_dir=SRC_DIR, interval=INTERVAL)

    try:
        while True:
            inp = input("Backup?")
            if inp == "restore":
                restore_name = filedialog.askopenfilename(
                    initialdir=BACKUP_PATH,
                    title="Select Zip",
                    filetypes=[('Compressed Files', '*.zip')]
                )
                P.restore(restore_name)
            P.backup()
    except KeyboardInterrupt:
        kill(TMR)
