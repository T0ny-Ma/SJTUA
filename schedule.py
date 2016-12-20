#-*- coding:utf-8 -*-
# DYNAMIC coded by Mr. Tang
# Create your classes here

import sys
from PySide import QtGui, QtCore
import sqlite3

affairList = []

class Calendar(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0, 60, 500, 540)
        self.initUI()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()
        painter.fillRect(rect, '#b0c4de')

    def initUI(self):
        self.cal = QtGui.QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.move(20, 20)
        self.cal.connect(self.cal, QtCore.SIGNAL('selectionChanged()'),self.showDate)
        self.label = QtGui.QLabel(self)
        date = self.cal.selectedDate()
        self.label.setText(date.toString("yyyy/MM/dd"))  # str(date.toPyDate())
        self.label.move(130, 260)
        self.cal.setGeometry(10, 50, 380, 300)
        self.update()


    def showDate(self):
        date = self.cal.selectedDate()
        self.label.setText(date.toString("yyyy/MM/dd"))


class Affair:
    def __init__(self, m):
        aid, bgntime, endtime,content = m
        self.aid = aid
        self.bgntime = bgntime
        self.endtime = endtime
        self.content = content

    def getIcon(self):
        iconid = int(self.aid) % 4
        return './head/' + str(iconid) + '.png'


class AffairDB:
    def __init__(self):
        conn = sqlite3.connect('test.db')
        self.cu = conn.cursor()
        self.affairList = []
        self.readAffair()

    def readAffair(self):
        self.affairList = []
        self.cu.execute("select  aid, bgntime, endtime,content from affair")
        for row in self.cu:
            m = Affair(row)
            self.affairList.append(m)

    def addAffair(self, affair):
        try:
            data = affair.aid, affair.bgntime, affair.endtime, affair.content
            self.cu.execute("INSERT INTO affair (aid, bgntime, endtime,content) \
                  VALUES (?, ?, ?, ?)", data)
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True

    def delAffair(self, aid):
        try:
            self.cu.execute("DELETE FROM affair WHERE aid = %d" % (aid))
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True


class AffairList(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(400, 60, 600, 540)
        self.db = AffairDB()

        self.list_view = QtGui.QListView(self)
        self.list_view.setGeometry(0, 0, 600, 540)
        self.list_view.setSpacing(3)

        self.list_model = AffairListModel(self.db.affairList)
        self.list_view.setModel(self.list_model)
        self.list_view.setIconSize(QtCore.QSize(50, 50))


class AffairListModel(QtCore.QAbstractListModel):
    def __init__(self, affairList):
        super(AffairListModel, self).__init__()
        self._items = set()
        for item in affairList:
            self._items.add(item)
        self.items = list(self._items)

    def rowCount(self, parent):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self.items[index.row()]
        fullname, icon_path, user_data = item.content, item.getIcon(), item.aid

        if role == QtCore.Qt.DisplayRole:
            return fullname

        elif role == QtCore.Qt.DecorationRole:
            icon = QtGui.QIcon(icon_path)
            return icon

        elif role == QtCore.Qt.BackgroundColorRole:
            colorTable = [0x000000, 0xFFFFE0, 0xDCDCDC, 0xF0FFFF,
                          0xD1EEEE, 0xCDCDC1, 0x00FFFF, 0x00FF7F]
            cc = (item.aid) % 8
            color = QtGui.QColor(colorTable[cc])
            return QtGui.QBrush(color)

        return None