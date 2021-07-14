from datetime import datetime, timedelta
from typing import Iterable


def seconds_to_timestr(seconds: int, show_seconds=False):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if show_seconds:
        return f"%i:%.2i:%.2i" % (hours, minutes, seconds)
    return "%i:%.2i" % (hours, minutes)

def daterange(start_date, end_date) -> Iterable[datetime]:
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)
