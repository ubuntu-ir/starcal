#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scal2 import core
from scal2.core import convert
from scal2.locale_man import tr as _

from scal2 import event_man

from scal2 import ui
from scal2.ui_gtk.mywidgets.multi_spin_button import DateButton
from scal2.ui_gtk.event import common

import gtk
from gtk import gdk

class EventWidget(common.EventWidget):
    def __init__(self, event):
        common.EventWidget.__init__(self, event)
        ###
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label(_('Date')), 0, 0)
        self.dateInput = DateButton()
        hbox.pack_start(self.dateInput, 0, 0)
        self.pack_start(hbox, 0, 0)
        #############
        #self.filesBox = common.FilesBox(self.event)
        #self.pack_start(self.filesBox, 0, 0)
    def updateWidget(self):
        common.EventWidget.updateWidget(self)
        self.dateInput.set_date(self.event.getDate())
    def updateVars(self):
        common.EventWidget.updateVars(self)
        self.event.setDate(*self.dateInput.get_date())
    def modeComboChanged(self, combo):## overwrite method from common.EventWidget
        newMode = combo.get_active()
        y, m, d = self.dateInput.get_date()
        self.dateInput.set_date(convert(y, m, d, self.event.mode, newMode))
        self.event.mode = newMode



