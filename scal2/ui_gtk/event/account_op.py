from scal2.locale_man import tr as _
from scal2 import event_lib
from scal2 import ui

from scal2.ui_gtk import *
from scal2.ui_gtk.utils import dialog_add_button, showError
from scal2.ui_gtk.event import makeWidget

class AccountEditorDialog(gtk.Dialog):
    def __init__(self, account=None):
        gtk.Dialog.__init__(self)
        self.set_title(_('Edit Account') if account else _('Add New Account'))
        ###
        dialog_add_button(self, gtk.STOCK_CANCEL, _('_Cancel'), gtk.RESPONSE_CANCEL)
        dialog_add_button(self, gtk.STOCK_OK, _('_OK'), gtk.RESPONSE_OK)
        ##
        self.connect('response', lambda w, e: self.hide())
        #######
        self.account = account
        self.activeWidget = None
        #######
        hbox = gtk.HBox()
        combo = gtk.combo_box_new_text()
        if not ui.eventAccounts.accountTypesData:
            showError(_('No account plugins found'))
            return
        for name, desc in ui.eventAccounts.accountTypesData:
            combo.append_text(_(desc))
        pack(hbox, gtk.Label(_('Account Type')))
        pack(hbox, combo)
        pack(hbox, gtk.Label(''), 1, 1)
        pack(self.vbox, hbox)
        ####
        if self.account:
            self.isNew = False
            combo.set_active(event_lib.classes.account.names.index(self.account.name))
        else:
            self.isNew = True
            cls = ui.eventAccounts.getFirstClass()
            if not cls:
                showError(_('Account class is empty'))
                return
            self.account = cls()
            combo.set_active(0)
        self.activeWidget = None
        combo.connect('changed', self.typeChanged)
        self.comboType = combo
        self.vbox.show_all()
        self.typeChanged()
    def dateModeChanged(self, combo):
        pass
    def typeChanged(self, combo=None):
        if self.activeWidget:
            self.activeWidget.updateVars()
            self.activeWidget.destroy()
        cls = event_lib.classes.account[self.comboType.get_active()]
        account = cls()
        if self.account:
            account.copyFrom(self.account)
            account.setId(self.account.id)
            del self.account
        if self.isNew:
            account.title = cls.desc ## FIXME
        self.account = account
        self.activeWidget = makeWidget(account)
        pack(self.vbox, self.activeWidget)
    def run(self):
        if self.activeWidget is None or self.account is None:
            return None
        if gtk.Dialog.run(self) != gtk.RESPONSE_OK:
            return None
        self.activeWidget.updateVars()
        self.account.save()
        if self.isNew:
            event_lib.lastIds.save()
        else:
            ui.eventAccounts[self.account.id] = self.account
        self.destroy()
        return self.account


class FetchRemoteGroupsDialog(gtk.Dialog):
    def __init__(self, account):
        gtk.Dialog.__init__(self)
        self.account = account


