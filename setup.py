#!/usr/bin/env python3

from distutils.core import setup
import subprocess
import glob

setup(
    name='timetracker',
    version='0.1',
    description='Track time spent on tasks',
    license='GPLv3',
    scripts=['scripts/timetracker'],
    packages=['timetracker'],
    data_files=[
        ('/usr/local/share/timetracker/ui', glob.glob('ui/*')),
        ('/usr/local/share/applications', ['data/timetracker.desktop']),
    ],
    requires=['gi'],
)

subprocess.check_call(["update-desktop-database", "/usr/local/share/applications"])
