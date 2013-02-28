from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qc

qfontDecode = lambda qfont: (
    str(qfont.family()),
    qfont.bold(),
    qfont.italic(),
    qfont.pointSize()
)

qfontEncode = lambda font: qt.QFont(
    font[0],
    font[3],
    qt.QFont.Bold if font[1] else qt.QFont.Normal,
    font[2]
)

def fontToStr(font):
    s = font[0]
    if font[1]:
        s += ' Bold'
    if font[2]:
        s += ' Italic'
    return s + ' %s'%font[3]


def qfontToStr(qfont):
    s = qfont.family()
    if qfont.bold():
        s += ' Bold'
    if qfont.italic():
        s += ' Italic'
    return s + ' %s'%qfont.pointSize()




