# -*- coding:utf-8 -*-

import re
import sys
import glob
import os
from PySide import QtCore, QtGui
import sqlite3

memberList=[]


class Member:
    def __init__(self, m):     # pid = 0, name = "lazy", phone = '', email = ''
        pid, name, phone, email = m
        self.pid = pid
        self.name = name
        self.phone = phone
        self.email = email

    def getIcon(self):
        iconid = int(self.pid) % 4
        return './head/' + str(iconid) + '.png'


class MemberDB:
    def __init__(self):
        conn = sqlite3.connect('test.db')
        self.cu = conn.cursor()
        self.memberList = []
        self.readMember()

    def readMember(self):
        self.memberList = []
        self.cu.execute("select pid, name, phone, email from member")
        for row in self.cu:
            m = Member(row)
            self.memberList.append(m)

    def addMember(self, member):
        try:
            data = member.pid, member.name, member.phone, member.email
            self.cu.execute("INSERT INTO member (pid,name,phone,email) VALUES (?, ?, ?, ?)", data)
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True

    def delMember(self, pid):
        try:
            self.cu.execute("DELETE FROM member WHERE pid = %d" % (pid))
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True


    def searchMember(self,tags):
        self.memberList = []


class MemberLocate(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0, 60, 700, 540)
        self.db = MemberDB()

        self.lineedit = QtGui.QLineEdit(self)
        self.lineedit.setGeometry(10, 5, 450, 35)

        self.lineedit.returnPressed.connect(self._lineedit_returnPressed)
        self.lineedit.textChanged.connect(self._lineedit_textChanged)

        self.list_view = QtGui.QListView(self)
        self.list_view.setGeometry(10, 75, 680, 465)
        self.list_view.setSpacing(3)

        self.list_model = MemberListModel(self.db.memberList)
        self.list_view.setModel(self.list_model)
        self.list_view.setIconSize(QtCore.QSize(50, 50))



    def _lineedit_textChanged(self, text):
        print "text changed:", text

        self.item_box.filter_list_by_keyword(text)
        self.list_view.update()

    def _lineedit_returnPressed(self):
        text = self.lineedit.text()

        print "return press:", text
        print "items:", self.item_box.items


class MemberListModel(QtCore.QAbstractListModel):
    def __init__(self, memberList):
        super(MemberListModel, self).__init__()
        self._items = set()
        for item in memberList:
            self._items.add(item)
        self.items = list(self._items)

    def rowCount(self, parent):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self.items[index.row()]
        fullname, icon_path, user_data = item.name, item.getIcon(), item.pid

        if role == QtCore.Qt.DisplayRole:
            return fullname

        elif role == QtCore.Qt.DecorationRole:
            icon = QtGui.QIcon(icon_path)
            return icon

        elif role == QtCore.Qt.BackgroundColorRole:
            colorTable = [0xD1EE22, 0xFFFFE0, 0xDCDCDC, 0xF0FFFF,
                          0xD1EEEE, 0xCDCDC1, 0x00FFFF, 0x00FF7F]
            cc = item.pid % 8
            color = QtGui.QColor(colorTable[cc])
            return QtGui.QBrush(color)

        return None








