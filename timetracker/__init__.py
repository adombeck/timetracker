from pathlib import Path

DATA_DIR = Path(Path.home(), ".local/share/timetracker")
TASK_DIR = Path(DATA_DIR, "tasks")
UI_DIR = Path("/usr/local/share/timetracker/ui")
NEW_TASK_DIALOG_PATH = Path(UI_DIR, "new-task-dialog.ui")
