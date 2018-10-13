from gi.repository import Gio, GLib
from logging import getLogger

logger = getLogger(__name__)


class ScreenlockMonitor(object):
    watcher_id = None  # type: int
    subscription_id = None  # type: int
    connection = None  # type: Gio.DBusConnection

    def __init__(self, app):
        self.app = app
        self.connection = Gio.bus_get_sync(Gio.BusType.SESSION, cancellable=None)

    def start(self):
        self.watcher_id = Gio.bus_watch_name_on_connection(
            self.connection,
            name="org.gnome.ScreenSaver",
            flags=Gio.BusNameWatcherFlags.NONE,
            name_appeared_closure=self.on_name_appeared,
            name_vanished_closure=self.on_name_vanished
        )

    def stop(self):
        if self.subscription_id:
            self.connection.signal_unsubscribe(self.subscription_id)
            self.subscription_id = None

        if self.watcher_id:
            Gio.bus_unwatch_name(self.watcher_id)
            self.watcher_id = None

    def on_name_appeared(self, connection: Gio.DBusConnection, name: str, name_owner: str):
        self.subscription_id = connection.signal_subscribe(
            sender=name_owner,
            interface_name="org.gnome.ScreenSaver",
            member="ActiveChanged",
            object_path="/org/gnome/ScreenSaver",
            arg0=None,
            flags=Gio.DBusSignalFlags.NONE,
            callback=self.on_active_changed
        )

    def on_name_vanished(self):
        pass

    def on_active_changed(self, connection: Gio.DBusConnection,
                          sender_name: str,
                          object_path: str,
                          interface_name: str,
                          signal_name: str,
                          parameters: GLib.Variant):
        activated = parameters.unpack()[0]
        self.on_screen_was_locked() if activated else self.on_screen_was_unlocked()

    def on_screen_was_locked(self):
        logger.info("Screen was locked")
        # We only stop the timer, but don't send a notification, because we don't
        # want the notification to wake up the system when it has just been locked
        self.app.timer.stop()

    def on_screen_was_unlocked(self):
        logger.info("Screen was unlocked")
        self.app.start_clocking()
