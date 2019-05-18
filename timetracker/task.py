import logging
from pathlib import Path
from typing import Union, List
from datetime import datetime
import shutil

from timetracker import DATA_DIR, TASK_DIR, TIME_FORMAT, DATE_FORMAT
from timetracker import util


logger = logging.getLogger(__name__)


class Task(object):
    last = Path(DATA_DIR, "last")

    def __init__(self, name):
        self.name = name
        self.path = Path(TASK_DIR, "name").with_name(name)

    @classmethod
    def get_last(cls) -> Union["Task", None]:
        try:
            name = cls.last.read_text()
        except FileNotFoundError:
            return None

        return cls(name)

    @classmethod
    def set_last(cls, task: "Task"):
        cls.last.write_text(task.name)

    @classmethod
    def get_all(cls) -> List["Task"]:
        names = sorted(path.name for path in TASK_DIR.iterdir())
        return [Task(name) for name in names]

    def exists(self) -> bool:
        return self.path.exists()

    def create(self):
        logger.info("Creating task '%s'", self.name)
        self.path.touch(0o700)

    def create_backup(self):
        logger.info("Creating backup of '%s'", self.path)
        backup_path = str(self.path) + ".bkp"
        shutil.copy(self.path, backup_path)

    def new_entry(self, start_time: datetime):
        start_time_str = start_time.strftime(TIME_FORMAT)
        logger.info("Inserting new entry to task '%s': %s", self.name, start_time_str)

        lines = self.path.read_text().strip().split("\n")
        lines.append("%s - %s: 0:00:00\n" % (start_time_str, start_time_str))
        self.path.write_text("\n".join(lines))

    def update_entry(self, start_time: datetime, current_time: datetime):
        self.create_backup()

        start_time_str = start_time.strftime(TIME_FORMAT)
        current_time_str = current_time.strftime(TIME_FORMAT)
        delta = current_time - start_time
        duration_str = util.seconds_to_timestr(delta.seconds, show_seconds=True)
        logger.info("Updating last entry of task '%s': %s", self.name, duration_str)

        lines = self.path.read_text().strip().split("\n")
        if not lines[-1].startswith(start_time_str):
            raise ValueError("last entry of task '%s' does not have start time '%s", self.name, start_time_str)
        lines[-1] = "%s - %s: %s\n" % (start_time_str, current_time_str, duration_str)
        self.path.write_text("\n".join(lines))

    def get_sum(self, from_: datetime = None, to: datetime = None) -> int:
        if from_ is None:
            from_ = datetime.min
        if to is None:
            to = datetime.max
        total_seconds = 0

        for line in self.path.read_text().strip().split("\n"):
            date_str = line.split()[0]
            if not from_ <= datetime.strptime(date_str, DATE_FORMAT) <= to:
                continue
            duration_str = line.split(": ")[-1]
            hours, minutes, seconds = (int(s) for s in duration_str.split(":"))
            total_seconds += seconds + 60 * minutes + 3600 * hours

        return total_seconds
