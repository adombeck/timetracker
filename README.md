# timetracker
Basic GTK time tracker app

##  Installation

1. Run setup.py:
   ```
   sudo ./setup.py install
   ```

2. Add keyboard shortcuts to create a new task (`timetracker --new`) and
   to toggle clocking (`timetracker --toggle`).


## Usage

1. Use keyboard shortcut to create a new task.

   ![Screenshot of the new task dialog](https://github.com/adombeck/timetracker/blob/main/images/new-task.png?raw=true)
   
   An icon indicating the clocking status will be shown in the panel
   (requires AppIndicator support, on Debian you can use 
   [`gnome-shell-extension-appindicator`](https://packages.debian.org/sid/gnome-shell-extension-appindicator)).
   
2. Use keyboard shortcut to toggle clocking.
   
   ![Screenshot of the clocking toggle notification](https://github.com/adombeck/timetracker/blob/main/images/stopped-clocking.png?raw=true)

3. To clock another, previously created task, use the keyboard shortcut
   to create a new task and select the task from the list. 
   
   ![Screenshot of new task dialog with previous tasks](https://github.com/adombeck/timetracker/blob/main/images/previous-task.png?raw=true)

4. Print a timesheet:
   ```
   $ timetracker --print-timesheet 2024-01-01,2024-03-31 --filter "sysadmin.*"
   sysadmin #1234 - Example task: 0:30
   total: 0:30
   ```
5. Open tasks directory via the AppIndicator menu to manually inspect 
   and edit the tasks.
   
   ![Screenshot of the AppIndicator menu](https://github.com/adombeck/timetracker/blob/main/images/app-indicator-menu.png?raw=true)