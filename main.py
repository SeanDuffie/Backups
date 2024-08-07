""" @file main.py
    @author Sean Duffie
    @brief 
"""
import logging
import os
from tkinter import filedialog

import log_format
from pipeline import Pipeline
from scheduler import Scheduler

### PATH SECTION ###
DEFAULT_PATH = os.path.dirname(__file__)
ACTIVE_PATH = f"{DEFAULT_PATH}/project/"
BACKUP_PATH = f"{DEFAULT_PATH}/backups/"


### LOGGING SECTION ###
logname = ACTIVE_PATH + '/' + 'MCSERVER.log'
log_format.format_logs(logger_name="MCLOG", file_name=logname)
logger = logging.getLogger("MCLOG")


src_dir = filedialog.askdirectory(
    title="Select Backup Location",
    initialdir=f"{DEFAULT_PATH}/"
)
if src_dir == "":
    src_dir = ACTIVE_PATH

p = Pipeline(src_dir=src_dir, zip_dir=BACKUP_PATH)
s = Scheduler(interval=300, function=p.backup(), args=["Hourly"])
s.start()
