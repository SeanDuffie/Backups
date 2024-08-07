""" @file scheduler.py
    @author Sean Duffie
    @brief Scheduler thread wrapper class that runs the backup function on every interval
"""
import datetime
import logging
import threading

import log_format

### LOGGING SECTION ###
log_format.format_logs(logger_name="BACKUP")
logger = logging.getLogger("BACKUP")

class Scheduler(threading.Timer):
    """ Manages the frequency and intervals of calls to the backup function.
    Construct one for each interval by passing in the amount of 

    Inherits from the threading.Timer class
    """
    def __init__(self, interval, function, args=None, kwargs=None):
        threading.Timer.__init__(self, interval, function, args, kwargs)

        self.invl = datetime.timedelta(seconds=self.interval)
        self.start_time = 0
        self.tprev = 0
        self.tnext = 0

        logger.warning(
            "Seconds until First %s Backup: %s",
            *self.args,
            (self.tnext - self.tprev).total_seconds()
        )

    def next_time(self):
        """ Calculates the next timestamp that "run" will be active.

        Args:
            prev (datetime.datetime): Timestamp of last action.
            interval (datetime.timedelta): Seconds in between actions.

        Returns:
            datetime.datetime: Timestamp of the next run.
        """
        nxt = self.tprev + self.interval
        logger.info(
            "Next %s Backup time is at %s (currently %s)",
            *self.args,
            nxt,
            datetime.datetime.now()
        )
        return nxt

    def get_remaining(self):
        """ Calculates and returns time remaining before next backup.

        Returns:
            datetime.timedelta: Amount of time remaining before next backup.
        """
        return self.tnext - datetime.datetime.now()

    def run(self):
        """ Function callback that is launched whenever the Scheduler thread is started. """
        # Initial timestamps
        self.start_time = datetime.datetime.now()
        self.tprev = self.start_time
        self.tnext = self.next_time()

        # Timer loop
        while not self.finished.wait((self.tnext - self.tprev).total_seconds()):
            self.tprev = self.tnext
            self.tnext = self.next_time()

            self.function(*self.args, **self.kwargs)
        logger.info("Scheduler finished.")
