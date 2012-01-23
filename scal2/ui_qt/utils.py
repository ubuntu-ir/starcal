from subprocess import Popen
from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qc

def hideList(widgets):
    for w in widgets:
        w.hide()

def showList(widgets):
    for w in widgets:
        w.show()


