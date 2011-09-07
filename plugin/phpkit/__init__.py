# -*- coding: utf-8 -*-

import gtk
import gedit


class PHPKitPlugin(gedit.Plugin):

    WINDOW_DATA_KEY = "PHPKitData"

    def __init__(self):
        gedit.Plugin.__init__(self)

    def activate(self, window):
        helper = PHPKit(self, window)
        window.set_data(self.WINDOW_DATA_KEY, helper)

    def deactivate(self, window):
        window.get_data(self.WINDOW_DATA_KEY).deactivate()
        window.set_data(self.WINDOW_DATA_KEY, None)

    def update_ui(self, window):
        window.get_data(self.WINDOW_DATA_KEY).update_ui()


class PHPKit:

    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin

        self._provider = None

    def deactivate(self):
        self._provider = None
        self._window = None
        self._plugin = None

    def update_ui(self):
        pass
