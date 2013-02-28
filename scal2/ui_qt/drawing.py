from scal2 import ui

from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qc

from scal2.ui_qt.font_utils import *


def calcTextWidth(text, arg=None):
    if isinstance(text, str):
        text = text.decode('utf-8')
    if arg==None:
        qfont = qfontEncode(ui.getFont())
    elif isinstance(arg, tuple):
        qfont = qfontEncode(arg)
    elif isinstance(arg, qt.QWidget):
        qfont = arg.font()
    elif isinstance(arg, qt.QFont):
        qfont = arg
    n = len(text)
    met = qt.QFontMetrics(qfont)
    ## OR widget.fontMetrics()
    ## OR app.fontMetrics()
    w = 0
    for i in range(n):
        w += met.charWidth(text, i)
    return w



## def newTextLayout(widget, text='', font=None): ????????



