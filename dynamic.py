#-*- coding:utf-8 -*-
# DYNAMIC coded by Mr. Gong
# Create your classes here
# you may use :
from PySide import QtCore, QtGui
import sqlite3


class Dynamic:
    def __init__(self, m):
        dnid, bgntime, endtime, content, pointer = m
        self.dnid = dnid
        self.bgntime = bgntime
        self.endtime = endtime
        self.content = content
        self.pointer = pointer

    def getIcon(self):
        iconid = int(self.dnid) % 4
        return './head/' + str(iconid) + '.png'


class DynamicDB:
    def __init__(self):
        conn = sqlite3.connect('test.db')
        self.cu = conn.cursor()
        self.dynamicList = []
        self.readDynamic()

    def readDynamic(self):
        self.dynamicList = []
        self.cu.execute("select dnid, bgntime, endtime, content, pointer from dynamic")
        for row in self.cu:
            m = Dynamic(row)
            self.dynamicList.append(m)

    def addDynamic(self, dynamic):
        try:
            data = dynamic.dnid, dynamic.bgntime, dynamic.endtime, dynamic.content, dynamic.pointer
            self.cu.execute("INSERT INTO dynamic (dnid, bgntime, endtime, content, pointer)\
                   VALUES (?, ?, ?, ?, ?)", data)
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True

    def delDynamic(self, dnid):
        try:
            self.cu.execute("DELETE FROM dynamic WHERE dnid = %d" % (dnid))
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True


class DynamicList(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0, 60, 1000, 540)
        self.db = DynamicDB()

        self.list_view = QtGui.QListView(self)
        self.list_view.setGeometry(0, 0, 1000, 540)
        self.list_view.setSpacing(3)
        self.list_view.setGridSize(QtCore.QSize(100, 100))

        self.list_model = DynamicListModel(self.db.dynamicList)
        self.list_view.setModel(self.list_model)
        self.list_view.setIconSize(QtCore.QSize(50, 50))


class DynamicListModel(QtCore.QAbstractListModel):
    def __init__(self, dynamicList):
        super(DynamicListModel, self).__init__()
        self._items = set()
        for item in dynamicList:
            self._items.add(item)
        self.items = list(self._items)

    def rowCount(self, parent):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self.items[index.row()]
        fullname, icon_path, user_data = item.content, item.getIcon(), item.dnid
        fullname = item.content + 5 * "\n"

        if role == QtCore.Qt.DisplayRole:
            return fullname

        #elif role == QtCore.Qt.DecorationRole:
            #icon = QtGui.QIcon(icon_path)
            #return icon

        elif role == QtCore.Qt.BackgroundColorRole:
            colorTable = [0xcdcdcd, 0xc0d9d9, 0x70DBDB, 0xF0FFFF,
                          0xD1EEEE, 0xCDCDC1, 0x00FFFF, 0x00FF7F]
            cc = item.dnid % 8
            color = QtGui.QColor(colorTable[cc])
            return QtGui.QBrush(color)

        return None

