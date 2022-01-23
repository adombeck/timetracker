#!/usr/bin/env python3
import sys

from setuptools import setup
from setuptools.command.install import install
import subprocess
import glob


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        subprocess.check_call(["update-desktop-database", "/usr/local/share/applications"])

        print('''
To add GNOME keybindings (given that set-gnome-keybinding.py is installed), run:

set-gnome-keybinding.py "Start clocking new task" "timetracker --new" "F7"
set-gnome-keybinding.py "Toggle clocking" "timetracker --toggle" "F8"
''', file=sys.stderr)


setup(
    cmdclass={
        'install': PostInstallCommand,
    },
    name='timetracker',
    version='0.1',
    description='Track time spent on tasks',
    license='GPLv3',
    scripts=['scripts/timetracker'],
    packages=['timetracker'],
    data_files=[
        ('/usr/local/share/timetracker/icons', glob.glob('icons/*')),
        ('/usr/local/share/timetracker/ui', glob.glob('ui/*')),
        ('/usr/local/share/applications', ['data/timetracker.desktop']),
    ],
    requires=['gi'],
)
