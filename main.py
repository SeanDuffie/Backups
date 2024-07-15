""" @file main.py
    @author Sean Duffie
    @brief 
"""
import logging

import logFormat
from backup import Pipeline
from schedule import Scheduler

### LOGGING SECTION ###
logFormat.format_logs(logger_name="BACKUP")
logger = logging.getLogger("BACKUP")

def launch(proj_dir: str, interval: int = 1800):
    logging.info("Configuring Backup: Every %d minutes from %s to %s", interval/60, proj_dir, back_dir)
    pipeline = Pipeline()
    tmr = Scheduler(interval, pipeline.backup)
    tmr.setProj(proj_dir)
    tmr.start()
    return tmr

def kill(tmr: Scheduler):
    tmr.cancel()

if __name__ == "__main__":
    try:
        TMR = launch()
    except KeyboardInterrupt:
        kill(TMR)
