#-*- coding:utf-8 -*-
# DYNAMIC coded by Mr. Gong
# Create your classes here
# you may use :
from PySide import QtCore, QtGui
import sqlite3
import sys


class Dynamic:
    def __init__(self, m):
        dnid, bgntime, endtime, title, content, pointer = m
        self.dnid = dnid
        self.bgntime = bgntime
        self.endtime = endtime
        self.title = title
        self.content = content
        self.pointer = pointer

    def getIcon(self):
        iconid = int(self.dnid) % 4
        return './head/' + str(iconid) + '.png'


class DynamicDB:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cu = self.conn.cursor()
        self.maxid = 0
        self.dynamicList = []
        self.readDynamic()

    def readDynamic(self):
        self.dynamicList = []
        self.cu.execute("select dnid, bgntime, endtime, title, content, pointer from dynamic")
        for row in self.cu:
            m = Dynamic(row)
            self.dynamicList.append(m)
            self.maxid = max(m.dnid, self.maxid)

    def newDynamic(self):
        try:
            t = QtCore.QTime()
            now_time = t.currentTime().toString()
            # some bug here lastid to maxid
            data = self.maxid + 1, now_time, now_time, u"新动态", u"待编辑", ""
            self.cu.execute("INSERT INTO dynamic (dnid, bgntime, endtime, title, content, pointer)\
                   VALUES (?, ?, ?, ?, ?, ?)", data)
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True

    def setDynamic(self, dynamic):
        try:
            data = dynamic.dnid, dynamic.bgntime, dynamic.endtime, dynamic.title, dynamic.content, dynamic.pointer
            self.cu.execute("INSERT INTO dynamic (dnid, bgntime, endtime, title, content, pointer)\
                   VALUES (?, ?, ?, ?, ?, ?)", data)
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

        self.list_view = DynamicListView(self)
        self.list_view.setGeometry(0, 0, 1000, 540)

        self.popup_menu = QtGui.QMenu(self)

        self.menu_add_act = QtGui.QAction(u"新建", self)
        self.menu_add_act.triggered.connect(self.add_cb)
        self.popup_menu.addAction(self.menu_add_act)

        self.menu_delete_act = QtGui.QAction(u"删除", self)
        self.menu_delete_act.triggered.connect(self.delete_cb)
        self.popup_menu.addAction(self.menu_delete_act)

        self.popup_menu.addSeparator()

        self.menu_edit_act = QtGui.QAction(u"编辑", self)
        self.menu_edit_act.triggered.connect(self.edit_cb)
        self.popup_menu.addAction(self.menu_edit_act)

    def add_cb(self):
        self.list_view.addItem()

    def delete_cb(self):
        self.list_view.delItem()

    def edit_cb(self):
        self.list_view.hide()
        item = self.list_view.curItem()
        self.editor = DynamicEditor(self, item)

    def contextMenuEvent(self, event):
        point = self.mapToGlobal(event.pos())
        act = self.popup_menu.exec_(point)

        if act == self.menu_add_act:
            print "menu add clicked"
        elif act == self.menu_delete_act:
            print "menu delete clicked"
        elif act == self.menu_edit_act:
            print "menu edit clicked"

        return super(DynamicList, self).contextMenuEvent(event)



class DynamicListView(QtGui.QListView):
    def __init__(self, parent):
        QtGui.QListView.__init__(self, parent)
        self.db = DynamicDB()
        self.setSpacing(5)
        font = QtGui.QFont()
        font.setFamily("Song Typeface")
        font.setPointSize(18)
        self.setFont(font)

        self.list_model = DynamicListModel(self.db.dynamicList)
        self.setModel(self.list_model)
        self.preIndex = 0
        self.curIndex = 0

    def addItem(self):
        self.db.newDynamic()
        self.refList()

    def delItem(self):
        # some bug here , index reset error when menu click
        # print "I want to del ",self.preIndex
        index = self.preIndex
        dnid = self.list_model.items[index].dnid
        self.db.delDynamic(dnid)
        self.refList()

    def editItem(self, dynamic):
        self.db.delDynamic(dynamic.dnid)
        self.db.setDynamic(dynamic)
        self.refList()

    def curItem(self):
        index = self.preIndex
        return self.list_model.items[index]

    def refList(self):
        self.db.readDynamic()
        self.list_model.items = self.db.dynamicList

    def currentChanged(self, current, previous):
        index = self.currentIndex().row()
        self.list_model.setIndex(index)
        self.preIndex = self.curIndex
        self.curIndex = index


class DynamicListModel(QtCore.QAbstractListModel):
    def __init__(self, dynamicList):
        super(DynamicListModel, self).__init__()
        self.items = dynamicList
        self.curIndex = 0

    def setIndex(self,index):
        self.curIndex = index
        self.reset()

    def rowCount(self, parent):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        """try:
            item = self.items[index.row()]
        except IndexError:
            return"""
        item = self.items[index.row()]
        if index.row() == self.curIndex:
            text = u"%d ：%s\n%s\n\n%s" % (item.dnid, item.title, item.content, item.bgntime)
        else:
            text = u"%d ：%s\n\n%s" % (item.dnid, item.title, item.bgntime)

        if role == QtCore.Qt.DisplayRole:
            return text

        elif role == QtCore.Qt.BackgroundColorRole:
            colorTable = [0xcdcdcd, 0xc0d9d9, 0x70DBDB, 0xF0FFFF,
                          0xD1EEEE, 0xCDCDC1, 0x00FFFF, 0x00FF7F]
            cc = item.dnid % 8
            color = QtGui.QColor(colorTable[cc])
            return QtGui.QBrush(color)

        return None


class DynamicEditor(QtGui.QFrame):
    def __init__(self, parent, dynamic):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0, 0, 1000, 540)
        self.parent = parent
        self.dynamic = dynamic
        font = QtGui.QFont()
        font.setFamily("Song Typeface")
        font.setPointSize(18)

        self.label1 = QtGui.QLabel(u"编辑动态", self)
        self.label1.setGeometry(450, 0, 100, 50)
        self.label1.setFont(font)

        """self.label2 = QtGui.QLabel(u"主题：", self)
        self.label2.setGeometry(0, 50, 50, 35)
        font.setPointSize(14)
        self.label2.setFont(font)"""
        font.setPointSize(14)

        self.text_sub = QtGui.QLineEdit(self)
        self.text_sub.setGeometry(0, 50, 950, 34)
        self.text_sub.setText(dynamic.title)
        self.text_sub.setFont(font)

        self.save_btn = QtGui.QPushButton(u"保存", self)
        self.save_btn.setGeometry(950, 49, 52, 36)
        self.save_btn.clicked.connect(self._savebtn_clicked)
        self.save_btn.setFont(font)

        self.text_edit = QtGui.QTextEdit(self)
        self.text_edit.setGeometry(0, 85, 1000, 455)
        font.setPointSize(12)
        self.text_edit.setFont(font)
        self.text_edit.setText(dynamic.content)

        self.back_btn = QtGui.QPushButton(u"←", self)
        self.back_btn.setGeometry(950, 400, 30, 30)
        self.back_btn.clicked.connect(self._backbtn_clicked)

        self.show()

    def _backbtn_clicked(self):
        self.hide()
        self.parent.list_view.show()

    def _savebtn_clicked(self):
        self.dynamic.title = self.text_sub.text()
        self.dynamic.content = self.text_edit.toPlainText()
        t = QtCore.QTime()
        now_time = t.currentTime().toString()
        self.dynamic.bgntime = now_time
        self.hide()
        print self.dynamic.title
        self.parent.list_view.editItem(self.dynamic)
        self.parent.list_view.show()
