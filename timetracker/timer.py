from datetime import datetime, timedelta
from dateutil import tz
from typing import TYPE_CHECKING
import threading
import time

if TYPE_CHECKING:
    from timetracker.task import Task


class Timer(object):
    thread = None
    start_time = None
    task = None

    def start(self, task: "Task", additional_minutes: int = 0):
        if self.thread:
            self.thread.halt.set()

        self.task = task
        self.start_time = datetime.now(tz.tzlocal()) - timedelta(minutes=additional_minutes)

        self.task.new_entry(self.start_time)

        self.thread = TimingThread(self)
        self.thread.start()

    def stop(self):
        if self.task:
            self.update_time()
        if self.thread:
            self.thread.halt.set()

    def update_time(self):
        self.task.update_entry(self.start_time, datetime.now(tz.tzlocal()) - self.start_time)


class TimingThread(threading.Thread):
    def __init__(self, timer: Timer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = timer
        self.halt = threading.Event()
        self.daemon = True

    def run(self):
        while not self.halt.is_set():
            self.timer.update_time()
            time.sleep(60)
