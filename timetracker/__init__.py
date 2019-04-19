from pathlib import Path

DATA_DIR = Path(Path.home(), ".local/share/timetracker")
TASK_DIR = Path(DATA_DIR, "tasks")  # type: Path
UI_DIR = Path("/usr/local/share/timetracker/ui")
NEW_TASK_DIALOG_UI_PATH = Path(UI_DIR, "new-task-dialog.ui")

TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"
DATE_FORMAT = "%Y-%m-%d"