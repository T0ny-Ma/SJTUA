from PySide import QtCore, QtGui

t = QtCore.QDateTime()
now_time = t.currentDateTime().toString()
print now_time