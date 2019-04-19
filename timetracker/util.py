
def seconds_to_timestr(seconds: int, show_seconds=False):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if show_seconds:
        return f"%i:%.2i:%.2i" % (hours, minutes, seconds)
    return "%i:%.2i" % (hours, minutes)