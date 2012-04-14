# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Saeed Rasooli <saeed.gnu@gmail.com> (ilius)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/gpl.txt>.
# Also avalable in /usr/share/common-licenses/GPL on Debian systems
# or /usr/share/licenses/common/GPL3/license.txt on ArchLinux

from scal2.locale_man import tr as _

from scal2 import core
from scal2.core import myRaise
from scal2 import ui

import gtk
from gtk import gdk

from scal2.ui_gtk.utils import toolButtonFromStock
from scal2.ui_gtk import preferences
from scal2.ui_gtk.preferences import set_tooltip


class CustomizableWidgetWrapper:
    def __init__(self, widget, name, desc, items=None, optionsWidget=None, enable=True):
        self.widget = widget
        self._name = name
        self.desc = desc
        if not items:
            items = []
        self.items = items
        self.optionsWidget = optionsWidget
        self.enable = enable
        if self.optionsWidget:
            self.optionsWidget.show_all()
    updateVars = lambda self: None
    confStr = lambda self: ''
    def moveItemUp(self, i):## override this method for non-GtkBox containers
        self.widget.reorder_child(self.items[i].widget, i-1)## for GtkBox (HBox and VBox)
        self.items.insert(i-1, self.items.pop(i))
    onDateChange = lambda self: None

class MainWinItem(CustomizableWidgetWrapper):
    def __init__(self, *args, **kwargs):
        CustomizableWidgetWrapper.__init__(self, self, *args, **kwargs)
        self.myKeys = []
    onConfigChange = lambda self: None

class CustomizeDialog(gtk.Dialog):
    def __init__(self, items=[]):
        gtk.Dialog.__init__(self)
        self.set_title(_('Customize'))
        self.set_has_separator(False)
        self.connect('delete-event', self.close)
        closeB = self.add_button(gtk.STOCK_CLOSE, 0)
        if ui.autoLocale:
            closeB.set_label(_('_Close'))
            closeB.set_image(gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_BUTTON))
        closeB.connect('clicked', self.close)
        ###
        self.items = items
        self.activeOptionsWidget = None
        ###
        model = gtk.TreeStore(bool, str) ## (gdk.Pixbuf, str)
        treev = gtk.TreeView(model)
        ##
        self.model = model
        self.treev = treev
        ##
        treev.set_enable_tree_lines(True)
        treev.set_headers_visible(False)
        ##
        col = gtk.TreeViewColumn('Widget')
        ##
        cell = gtk.CellRendererToggle()
        cell.connect('toggled', self.enableCellToggled)
        col.pack_start(cell, expand=False)
        col.add_attribute(cell, 'active', 0)
        ##
        treev.append_column(col)
        col = gtk.TreeViewColumn('Widget')
        ##
        cell = gtk.CellRendererText()
        col.pack_start(cell, expand=False)
        col.add_attribute(cell, 'text', 1)
        ##
        treev.append_column(col)
        ###
        for item in items:
            itemIter = model.append(None)
            model.set(itemIter, 0, item.enable, 1, item.desc)
            for child in item.items:
                childIter = model.append(itemIter)
                model.set(childIter, 0, child.enable, 1, child.desc)
        ###
        hbox = gtk.HBox()
        vbox_l = gtk.VBox()
        vbox_l.pack_start(treev, 1, 1)
        hbox.pack_start(vbox_l, 1, 1)
        ###
        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
        size = gtk.ICON_SIZE_SMALL_TOOLBAR
        toolbar.set_icon_size(size)
        ## argument2 to image_new_from_stock does not affect
        ###
        tb = toolButtonFromStock(gtk.STOCK_GO_UP, size)
        set_tooltip(tb, _('Move up'))
        tb.connect('clicked', self.upClicked)
        toolbar.insert(tb, -1)
        ###
        tb = toolButtonFromStock(gtk.STOCK_GO_DOWN, size)
        set_tooltip(tb, _('Move down'))
        tb.connect('clicked', self.downClicked)
        toolbar.insert(tb, -1)
        ###
        hbox.pack_start(toolbar, 0, 0)
        self.vbox.pack_start(hbox, 1, 1)
        self.vbox_l = vbox_l
        ###
        self.widget = gtk.VBox() ## itemsBox
        for item in items:
            self.widget.pack_start(item.widget, 0, 0)
        self.widget.show_all()
        for item in items:
            if item.enable:
                for chItem in item.items:
                    if not chItem.enable:
                        chItem.widget.hide()
            else:
                item.widget.hide()
        ###
        self.vbox.connect('size-request', self.vboxSizeRequest)
        self.vbox.show_all()
        treev.connect('cursor-changed', self.treevCursorChanged)
    def vboxSizeRequest(self, widget, req):
        self.resize(self.get_size()[0], 1)
    def getItemByPath(self, path):
        if isinstance(path, basestring):
            path = [int(p) for p in path.split(':')]
        elif isinstance(path, (int, long)):
            path = [path]
        elif not isinstance(path, (tuple, list)):
            raise TypeError('argument %s given to getItemByPath has bad type'%path)
        item = self.items[path[0]]
        for i in path[1:]:
            item = item.items[i]
        return item
    def treevCursorChanged(self, treev):
        if self.activeOptionsWidget:
            try:
                self.vbox_l.remove(self.activeOptionsWidget)
            except:
                myRaise(__file__)
            self.activeOptionsWidget = None
        index_list = treev.get_cursor()[0]
        if not index_list:
            return
        item = self.getItemByPath(index_list)
        if item.optionsWidget:
            self.activeOptionsWidget = item.optionsWidget
            self.vbox_l.pack_start(item.optionsWidget, 0, 0)
            item.optionsWidget.show()
    def upClicked(self, button):
        model = self.model
        index_list = self.treev.get_cursor()[0]
        if not index_list:
            return
        i = index_list[-1]
        if len(index_list)==1:
            if i<=0 or i>=len(model):
                gdk.beep()
                return
            ###
            self.moveItemUp(i)
            model.swap(model.get_iter(i-1), model.get_iter(i))
            self.treev.set_cursor(i-1)
        else:
            if i<=0:
                gdk.beep()
                return
            ###
            root = self.getItemByPath(index_list[:-1])
            if i>=len(root.items):
                gdk.beep()
                return
            ###
            root.moveItemUp(i)
            index_list2 = index_list[:-1] + (i-1,)
            model.swap(model.get_iter(index_list), model.get_iter(index_list2))
            self.treev.set_cursor(index_list2)
    def downClicked(self, button):
        model = self.model
        index_list = self.treev.get_cursor()[0]
        if not index_list:
            return
        i = index_list[-1]
        if len(index_list)==1:
            if i<0 or i>=len(model)-1:
                gdk.beep()
                return
            ###
            self.moveItemUp(i+1)
            model.swap(model.get_iter(i), model.get_iter(i+1))
            self.treev.set_cursor(i+1)
        else:
            if i<0:
                gdk.beep()
                return
            ###
            root = self.getItemByPath(index_list[:-1])
            if i>=len(root.items)-1:
                gdk.beep()
                return
            ###
            root.moveItemUp(i+1)
            index_list2 = index_list[:-1] + (i+1,)
            model.swap(model.get_iter(index_list), model.get_iter(index_list2))
            self.treev.set_cursor(index_list2)
    def enableCellToggled(self, cell, path):
        active = not cell.get_active()
        self.model.set_value(self.model.get_iter(path), 0, active) ## or set(...)
        item = self.getItemByPath(path)
        item.enable = active
        if active:
            item.widget.show()
            item.onDateChange()
        else:
            item.widget.hide()
        if ui.mainWin:
            ui.mainWin.setMinHeight()
    def moveItemUp(self, i):
        self.widget.reorder_child(self.items[i].widget, i-1)## self.widget is VBox
        self.items.insert(i-1, self.items.pop(i))
    #def confStr(self):## FIXME
    def close(self, button=None, event=None):
        text = ''
        itemsData = []
        for item in self.items:
            item.updateVars()
            text += item.confStr()
            itemsData.append((item._name, item.enable))
        text += 'ui.mainWinItems=%r\n'%itemsData
        open(preferences.customizeConfPath, 'w').write(text) # FIXME
        self.hide()
        return True




