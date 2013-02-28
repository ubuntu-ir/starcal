from scal2 import ui

from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qc

from scal2.ui_qt.font_utils import qfontDecode

ui.initFonts(qfontDecode(qt.QApplication.font()))

