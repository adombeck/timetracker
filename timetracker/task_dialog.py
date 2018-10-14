from gi.repository import Gtk

from timetracker import NEW_TASK_DIALOG_UI_PATH
from timetracker.task import Task


class DialogCancelledError(Exception):
    pass


def completion_entry_match_func(completion: Gtk.EntryCompletion, key: str, iter: Gtk.TreeIter):
    return key.lower() in completion.get_model()[iter][0].lower()


def run_task_dialog() -> (str, str):
    builder = Gtk.Builder.new_from_file(str(NEW_TASK_DIALOG_UI_PATH))  # type: Gtk.Builder
    dialog = builder.get_object("dialog")  # type: Gtk.Dialog
    name_entry = builder.get_object("name_entry")  # type: Gtk.Entry
    additional_minutes_entry = builder.get_object("additional_minutes_entry")  # type: Gtk.Entry

    completion_model = Gtk.ListStore(str)
    for task in Task.get_all():
        completion_model.append([task.name])

    completion = Gtk.EntryCompletion()
    completion.set_model(completion_model)
    completion.set_text_column(0)
    completion.set_match_func(completion_entry_match_func)
    name_entry.set_completion(completion)

    result = dialog.run()
    dialog.close()

    if result != Gtk.ResponseType.OK:
        raise DialogCancelledError("Creating new task cancelled by the user")

    name = name_entry.get_text()
    additional_minutes_str = additional_minutes_entry.get_text()
    additional_minutes = int(additional_minutes_str) if additional_minutes_str else 0
    return name, additional_minutes
