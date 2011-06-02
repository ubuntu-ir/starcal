from subprocess import Popen
from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qc

def hideList(widgets):
    for w in widgets:
        w.hide()

def showList(widgets):
    for w in widgets:
        w.show()

def myUrlShow(link):
    try:
        Popen(['xdg-open', link])
    except:
        try:
            import webbrowser
            webbrowser.open(url)
        except:
            for path in ('/usr/bin/firefox', '/usr/bin/konqueror', '/usr/bin/gnome-www-browser', '/usr/bin/iceweasel'):
                if isfile(path):
                    Popen([path, link])
                    return

