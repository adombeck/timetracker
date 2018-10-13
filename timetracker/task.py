import logging
from pathlib import Path
from typing import Union, TYPE_CHECKING
import dateutil.parser


if TYPE_CHECKING:
    from datetime import datetime, timedelta

from timetracker import DATA_DIR


logger = logging.getLogger(__name__)


class Task(object):
    last = Path(DATA_DIR, "last")

    def __init__(self, name):
        self.name = name
        self.path = Path(DATA_DIR, "tasks", "name").with_name(name)

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

    def exists(self) -> bool:
        return self.path.exists()

    def create(self):
        logger.info("Creating task '%s'", self.name)
        self.path.touch(0o700)

    def new_entry(self, start_time: "datetime"):
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        logger.info("Inserting new entry to task '%s': %s", self.name, start_time_str)

        lines = self.path.read_text().strip().split("\n")
        lines.append("%s: 0:00\n" % start_time_str)
        self.path.write_text("\n".join(lines))

    def update_entry(self, start_time: "datetime", time: "timedelta"):
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        minutes, seconds = divmod(time.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        duration_str = "%i:%.2i:%.2i" % (hours, minutes, seconds)
        logger.info("Updating last entry of task '%s': %s", self.name, duration_str)

        lines = self.path.read_text().strip().split("\n")
        if not lines[-1].startswith(start_time_str):
            raise ValueError("last entry of task '%s' does not have start time '%s", self.name, start_time_str)
        lines[-1] = "%s: %s\n" % (start_time_str, duration_str)
        self.path.write_text("\n".join(lines))

    def get_sum(self) -> int:
        total_seconds = 0
        for line in self.path.read_text().strip().split("\n"):
            duration_str = line.split(": ")[-1]
            hours, minutes, seconds = (int(s) for s in duration_str.split(":"))
            total_seconds += seconds + 60 * minutes + 3600 * hours

        return total_seconds
