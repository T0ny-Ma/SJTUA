#-*- coding:utf-8 -*-
# DYNAMIC coded by Mr. Ma & Mr. Gong
# Create your classes here
# you may use :
# from PySide import QtCore, QtGui

from PySide import QtCore, QtGui
from smtplib import *
from Tkinter import *
import tkMessageBox
import string
import sqlite3
import os
import sys


css = '''
div {
    line-height: 27px;
}
.nickname {
    color: #A52A2A;
    font-weight: bolder;
}
.ts {
    color: #7F7F7F;
}
'''


class Dialog:
    def __init__(self, m):
        gid, contain = m
        self.gid = gid
        self.contain = contain

    def getIcon(self):
        iconid = int(self.gid) % 4
        return './head/' + str(iconid) + '.png'


class DialogDB:
    def __init__(self):
        conn = sqlite3.connect('test.db')
        self.cu = conn.cursor()
        self.dialogList = []
        self.readDialog()

    def readDialog(self):
        self.dialogList = []
        self.cu.execute("select gid, contain from people")
        for row in self.cu:
            m = Dialog(row)
            self.dialogList.append(m)

    def addDialog(self, dialog):
        try:
            data = dialog.gid, dialog.contain
            self.cu.execute("INSERT INTO group (gid, contain) VALUES (?, ?)", data)
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True

    def delDialog(self, gid):
        try:
            self.cu.execute("DELETE FROM group WHERE gid = %d" % (gid))
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True



class DialogList(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0, 60, 255, 540)
        self.db = DialogDB()

        self.lineedit = QtGui.QLineEdit(self)
        self.lineedit.setGeometry(0, 0, 255, 35)

        self.lineedit.returnPressed.connect(self._lineedit_returnPressed)
        self.lineedit.textChanged.connect(self._lineedit_textChanged)

        self.list_view = QtGui.QListView(self)
        self.list_view.setGeometry(0, 35, 255, 505)
        self.list_view.setSpacing(3)

        self.list_model = DialogListModel(self.db.dialogList)
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


class DialogListModel(QtCore.QAbstractListModel):
    def __init__(self, dialogList):
        super(DialogListModel, self).__init__()
        self._items = set()
        for item in dialogList:
            self._items.add(item)
        self.items = list(self._items)

    def rowCount(self, parent):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self.items[index.row()]
        fullname, icon_path, user_data = item.ccontent, item.getIcon(), item.gid

        if role == QtCore.Qt.DisplayRole:
            return fullname

        elif role == QtCore.Qt.DecorationRole:
            icon = QtGui.QIcon(icon_path)
            return icon

        elif role == QtCore.Qt.BackgroundColorRole:
            colorTable = [0xD1EE22, 0xFFFFE0, 0xDCDCDC, 0xF0FFFF,
                          0xD1EEEE, 0xCDCDC1, 0x00FFFF, 0x00FF7F]
            cc = item.gid % 8
            color = QtGui.QColor(colorTable[cc])
            return QtGui.QBrush(color)

        return None


class Message:
    def __init__(self, data):
        mid, sender, receiver, sendtime, content, pointer = data
        self.mid = mid
        self.sender = sender
        self.receiver = receiver
        self.sendtime = sendtime
        self.content = content
        self.pointer = pointer

    def getIcon(self):
        iconid = int(self.mid) % 4
        return './head/' + str(iconid) + '.png'


class MessageDB:
    def __init__(self):
        conn = sqlite3.connect('test.db')
        self.cu = conn.cursor()
        self.messageList = []
        self.readMessage()

    def readMessage(self):
        self.messageList = []
        self.cu.execute("select mid, sender, receiver, sendtime, content, pointer from message")
        for row in self.cu:
            m = Message(row)
            self.messageList.append(m)

    def addMessage(self, message):
        try:
            data = message.mid, message.sender, message.receiver,\
                   message.sendtime, message.content, message.pointer
            self.cu.execute("INSERT INTO message (mid, sender, receiver, sendtime, content, pointer)\
                   VALUES (?, ?, ?, ?, ?, ?)", data)
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True

    def delMessage(self, mid):
        try:
            self.cu.execute("DELETE FROM message WHERE mid = %d" % (mid))
        except Exception, e:
            print e
            return None
        self.conn.commit()
        return True


class MessageList(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(265, 60, 745, 540)
        self.db = MessageDB()

        self.list_view = QtGui.QListView(self)
        self.list_view.setGeometry(0, 0, 745, 540)
        self.list_view.setSpacing(3)

        self.list_model = MessageListModel(self.db.messageList)
        self.list_view.setModel(self.list_model)
        self.list_view.setIconSize(QtCore.QSize(50, 50))


class MessageListModel(QtCore.QAbstractListModel):
    def __init__(self, messageList):
        super(MessageListModel, self).__init__()
        self._items = set()
        for item in messageList:
            self._items.add(item)
        self.items = list(self._items)

    def rowCount(self, parent):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self.items[index.row()]
        fullname, icon_path, user_data = item.content, item.getIcon(), item.dnid

        if role == QtCore.Qt.DisplayRole:
            return fullname

        elif role == QtCore.Qt.DecorationRole:
            icon = QtGui.QIcon(icon_path)
            return icon

        elif role == QtCore.Qt.BackgroundColorRole:
            colorTable = [0xCDCDC1, 0xFFFFE0, 0xDCDCDC, 0xF0FFFF,
                          0xD1EEEE, 0xCDCDC1, 0x00FFFF, 0x00FF7F]
            cc = item.dnid % 8
            color = QtGui.QColor(colorTable[cc])
            return QtGui.QBrush(color)

        return None


class MessageRecord(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(265, 60, 745, 540)
        self.parent = parent

        self.text_doc = QtGui.QTextDocument()
        self.text_doc.setDefaultStyleSheet(css)

        self.text_record = QtGui.QTextEdit(self)
        self.text_record.setGeometry(0, 0, 745, 540)
        self.text_record.setDocument(self.text_doc)
        self.text_record.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        #        self.text_edit.setReadOnly(True)
        self.log(msg=' ')
        self.log(msg='hello\nworld')
        self.log(msg='hello\nworld')
        self.log(msg=u'中文输入\n法 KDE 桌面环境')
        self.log(msg='hello\nworld')
        self.log(msg='hello\nworld')

        self.top_btn = QtGui.QPushButton(u"▲", self)
        self.top_btn.setGeometry(680, 250, 30, 30)
        self.top_btn.clicked.connect(self._topbtn_clicked)

        self.buttom_btn = QtGui.QPushButton(u"▼", self)
        self.buttom_btn.setGeometry(680, 280, 30, 30)
        self.buttom_btn.clicked.connect(self._buttombtn_clicked)

        self.plus_btn = QtGui.QToolButton(self)
        icon = QtGui.QIcon("plus.png")
        self.plus_btn.setIcon(icon)
        self.plus_btn.setIconSize(QtCore.QSize(24, 24))
        self.plus_btn.clicked.connect(self._plusbtn_clicked)
        self.plus_btn.move(677, 400)

        self.text_edit = QtGui.QTextEdit(self)
        self.text_edit.setGeometry(0, 0, 745, 505)
        self.text_edit.hide()

        self.show()

    def _topbtn_clicked(self):
        scroll_bar = self.text_record.verticalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())

    def _buttombtn_clicked(self):
        scroll_bar = self.text_record.verticalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

    def _plusbtn_clicked(self):
        self.hide()
        self.parent.EmailEditor.show()

    def log(self, nickname='foo', msg=None):
        t = QtCore.QTime()
        now_time = t.currentTime().toString()

        msg = msg.replace(os.linesep, '<br />')
        log = '''<div><span class="nickname">%s</span>&nbsp;&nbsp;<span class="ts">%s</span><p class="msg">%s</p></div>''' % \
              (nickname, now_time, msg)
        self.text_record.append(log)

        #        t = self.text_doc.toHtml()
        #        with open('log.txt', 'w') as f:
        #            f.write(t.toUtf8())

        #        # buf = t
        #        buf = QtCore.QString('<html><body>你好</body></html>'.decode('utf-8'))
        #        self.text_doc.setHtml(buf)

        #        t = self.text_doc.toHtml()
        #        with open('log2.txt', 'w') as f:
        #            f.write(t.toUtf8())


class EmailEditor(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(265, 60, 745, 540)
        self.parent = parent

        self.label1 = QtGui.QLabel(u"收件人：", self)
        self.label1.setGeometry(0, 0, 50, 35)
        self.label2 = QtGui.QLabel(u"发件人：", self)
        self.label2.setGeometry(0, 35, 50, 35)
        self.label2 = QtGui.QLabel(u"主题：", self)
        self.label2.setGeometry(0, 70, 50, 35)

        self.text_to = QtGui.QLineEdit(self)
        self.text_to.setGeometry(50, 0, 745, 35)
        self.text_from = QtGui.QLineEdit(self)
        self.text_from.setGeometry(50, 35, 745, 35)
        self.text_sub = QtGui.QLineEdit(self)
        self.text_sub.setGeometry(50, 70, 745, 35)

        self.text_edit = QtGui.QTextEdit(self)
        self.text_edit.setGeometry(0, 105, 745, 435)

        self.back_btn = QtGui.QPushButton(u"←", self)
        self.back_btn.setGeometry(680, 400, 30, 30)
        self.back_btn.clicked.connect(self._backbtn_clicked)

        self.send_btn = QtGui.QPushButton(u"发送", self)
        self.send_btn.setGeometry(680, 250, 30, 30)
        self.send_btn.clicked.connect(self._sendbtn_clicked)

        self.show()

    def _backbtn_clicked(self):
        self.hide()
        self.parent.MessageRecord.show()

    def _sendbtn_clicked(self):
        self.demo = Signin(self)
        self.demo.show()
        self.parent.pbar.show()

    def getInfo(self):
        return self.text_to.text(), self.text_sub.text(),self.text_edit.toPlainText()




class Signin(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Signin, self).__init__()
        self.parent = parent


        x, y, w, h = 500, 200, 400, 300
        self.setGeometry(x, y, w, h)
        self.setFixedSize(QtCore.QSize(400, 300))

        account_label = QtGui.QLabel("E-Mail:", self)
        x, y, w, h = 40, 40, 221, 30
        account_label.setGeometry(x, y, w, h)

        self.account_combox = QtGui.QComboBox(self)
        self.account_combox.setEditable(True)
        self.account_combox.setGeometry(70, 70, 200, 26)
        # self.connect(self.account_combox, QtCore.SIGNAL('currentIndexChanged(QString)'),
                    # self._account_combox_currentIndexChanged)

        password_label = QtGui.QLabel("Password:", self)
        password_label.setGeometry(40, 110, 62, 30)

        self.password_lineedit = QtGui.QLineEdit(self)
        self.password_lineedit.setGeometry(70, 140, 200, 22)
        self.password_lineedit.setEchoMode(QtGui.QLineEdit.Password)

        reset_password_label = QtGui.QLabel("tips", self)
        reset_password_label.setGeometry(300, 140, 130, 30)

        self.remember_me_checkbox = QtGui.QCheckBox("Remember me", self)
        self.remember_me_checkbox.setGeometry(40, 180, 140, 20)

        self.clear_btn = QtGui.QPushButton("Clear", self)
        self.clear_btn.setGeometry(20, 210, 114, 32)
        self.clear_btn.clicked.connect(self._clear_btn_cb)

        self.sign_in_btn = QtGui.QPushButton("Sign In", self)
        self.sign_in_btn.setGeometry(170, 210, 114, 32)
        self.sign_in_btn.clicked.connect(self._signin_btn_cb)

    def _account_combox_currentIndexChanged(self, text):
        if not text:
            self.password_lineedit.setText("")

    def _clear_btn_cb(self):
        self.account_combox.clearEditText()
        self.password_lineedit.setText("")

    def _signin_btn_cb(self):
        self.username = self.account_combox.currentText()
        self.password = self.password_lineedit.text()
        if len(self.username)==0 or len(self.password)==0 or "@" not in self.username:
            tkMessageBox.showwarning("Caution!","Invalid e-mail address or empty password, check please!")
            self.clear()
            return
        self.getSmtpHost()
        self.connect()

    def connect(self):
        'this method will try to connet the SMTP server according the current user'
        HOST = 'smtp.' + self.smtp + '.com'
        try:
            self.mySMTP = SMTP(HOST)
            self.mySMTP.login(self.username, self.password)
            # except SMTPConnectError:
        except Exception, e:
            tkMessageBox.showerror('Link ERROR!', '%s' % e)
            return
        self.mySendMail = sendMail(self.mySMTP, self.username)
        to, sub, text = self.parent.getInfo()
        self.mySendMail.sendMail(to, sub, text)

    def clear(self):
        self.account_combox.currentText().delete(0,END)
        self.password = self.password_lineedit.text(0,END)

    def getSmtpHost(self):
        'this method try to obtian the SMTP HOST according the user account'
        firstSplit = self.username.split('@')[1]
        self.smtp = firstSplit.split('.')[0]

class sendMail(object):
    'my send mail class'
    def __init__(self, smtp='', sender=''):
        self.smtp = smtp
        self.sender = sender

    def getMailInfo(self):
        self.sendTo = to
        self.subjectInfo = sub
        self.sendTextInfo = text

    def sendMail(self,to, sub, text):
        # self.getMailInfo()
        body = string.join(("From: %s" % self.sender, "To: %s" % to, "Subject: %s" % sub, "", text), "\r\n")
        try:
            self.smtp.sendmail(self.sender, [to], body)
        except Exception, e:
            tkMessageBox.showerr('Failed!:(', "%s" % e)
            return
        tkMessageBox.showinfo('Attention!', 'Send!:)')




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    demo = Signin()
    demo.show()

    sys.exit(app.exec_())

