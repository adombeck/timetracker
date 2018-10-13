#!/usr/bin/env python3


from timetracker import TASK_DIR
from timetracker.task import Task


def main():
    task_names = [path.name for path in TASK_DIR.iterdir()]
    tasks = [Task(name) for name in task_names]
    for task in tasks:
        seconds = task.get_sum()
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        print("%s: %i:%.2i" % (task.name, hours, minutes))


if __name__ == "__main__":
    main()
