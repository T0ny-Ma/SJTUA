#! python2
#-*- coding:utf-8 -*-

import sys
from PySide import QtCore, QtGui
import sqlite3
from quitdialog import *
from member import *
from dynamic import *
from message import *
from schedule import *
# from signin import *

# some bug here convert state
INITBUG, DYNAMIC, SCHEDULE, MESSAGE, MEMBER = range(5)
winState = INITBUG
assName = "SJTU_CC"


class mainWindow(QtGui.QMainWindow):
    def __init__(self, associate, state):
        super(mainWindow, self).__init__()
        self.state = state
        self.associate = associate
        self.settings = load_settings(settings_path)

        self.w = 1000
        self.h = 600
        self.setFixedSize(QtCore.QSize(self.w, self.h))

        self.setGeometry(0, 0, self.w, self.h)
        self.center()
        self.setWindowTitle('SJTUA')
        self.logo_icon = QtGui.QIcon("logo_SJTUA.png")
        self.setWindowIcon(self.logo_icon)

        self.sys_tray_icon = QtGui.QSystemTrayIcon(parent=self)
        self.sys_tray_icon.setIcon(self.logo_icon)
        self.sys_tray_icon.activated.connect(self.on_sys_tray_icon_clicked)
        self.sys_tray_icon.messageClicked.connect(self.on_sys_tray_icon_msg_clicked)
        self.sys_tray_icon.show()

        self.boards = []

        self.TitleBoard = TitleBoard(self, self.associate.name, winState)
        self.EmailEditor = EmailEditor(self)
        self.MessageRecord = MessageRecord(self)
        self.DialogList = DialogList(self)
        self.DynamicList = DynamicList(self)
        self.MemberLocate = MemberLocate(self)
        self.Calendar = Calendar(self)
        self.AffairList = AffairList(self)
        self.boards.extend([self.MemberLocate,self.DynamicList,self.Calendar,self.AffairList,
                            self.EmailEditor,self.DialogList,self.MessageRecord])
        self.convertState(state)  # bug if self.state

        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(0, 50, 1030, 2)
        self.pbar.setMaximum(0)
        self.pbar.setMinimum(0)
        self.pbar.hide()
        self.show()


    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
        (screen.height() - size.height()) / 2)

    def show_and_raise(self):
        self.show()
        self.raise_()

    def convertState(self, state):
        # or some bug here
        self.state = state
        for board in self.boards:
            board.hide()
        self.boards = []
        if state == DYNAMIC:
            self.boards.append(self.DynamicList)
            pass
        elif state == SCHEDULE:
            self.boards.append(self.Calendar)
            self.boards.append(self.AffairList)
            pass
        elif state == MESSAGE:
            self.boards.append(self.DialogList)
            self.boards.append(self.MessageRecord)
            self.boards.append(self.EmailEditor)
            pass
        elif state == MEMBER:
            self.boards.append(self.MemberLocate)
            #self.boards.append(self.MemberInfo)
            pass
        for board in self.boards:
            board.show()
        self.update()

    def dispose(self, cmd):
        pass

    @staticmethod
    def confirm_quit(main_win, close_evt=None):
        if main_win.settings["confirm"]:
            QuitConfirmDlg.popup_and_get_inputs(main_win, main_win.settings)
            save_settings(main_win.settings)

        if main_win.settings['x_action_is_quit']:
            if close_evt:
                close_evt.accept()

            return True
        else:
            if close_evt:
                close_evt.ignore()

            main_win.hide()

            return False

    def closeEvent(self, evt):
        self.confirm_quit(self, evt)

    def keyPressEvent(self, evt):
        close_win_cmd_w = (evt.key() == QtCore.Qt.Key_W and evt.modifiers() == QtCore.Qt.ControlModifier)
        close_win_esc = (evt.key() == QtCore.Qt.Key_Escape)

        if close_win_cmd_w or close_win_esc:
            self.close()

    def on_sys_tray_icon_clicked(self, activation_reason):
        assert activation_reason in (
            QtGui.QSystemTrayIcon.Trigger,
            QtGui.QSystemTrayIcon.DoubleClick,
            QtGui.QSystemTrayIcon.MiddleClick)

        self.show_and_raise()

    def on_sys_tray_icon_msg_clicked(self, *args, **kwargs):
        print 'msg clicked'

    def sys_tray_icon_show_msg(self, title, msg,
                               icon=QtGui.QSystemTrayIcon.MessageIcon(),
                               msecs=10000):
        if self.sys_tray_icon.supportsMessages():
            self.sys_tray_icon.showMessage(title, msg, icon, msecs)


class TitleBoard(QtGui.QFrame):
    def __init__(self, parent, assName, state):
        QtGui.QFrame.__init__(self, parent)
        self.parent = parent
        self.assName = assName
        self.state = state
        self.x, self.y, self.w, self.h = 0, 0, 1000, 50
        self.resize(self.w, self.h)
        self.rect = QtCore.QRect(self.x, self.y, self.w, self.h)
        self.setFrameRect(self.rect)
        self.initUI()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        parent.convertState(self.state)
        self.update()

    def initUI(self):
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        self.cbx = QtGui.QComboBox(self)
        self.cbx.addItem(assName)
        self.cbx.addItem(u"注销")
        self.cbx.setFont(font)
        self.cbx.currentIndexChanged.connect(self._cbx_currentIndexChanged)
        self.cbx.setGeometry(10, 5, 130, 40)

        font.setFamily("Song Typeface")
        font.setPointSize(18)
        self.btn1 = QtGui.QPushButton(u"动态", self)
        self.btn1.setFlat(True)
        self.btn1.clicked.connect(self._btn1_cb)
        self.btn1.setGeometry(345, 10, 75, 40)
        self.btn1.setFont(font)
        self.btn2 = QtGui.QPushButton(u"日程", self)
        self.btn2.setFlat(True)
        self.btn2.clicked.connect(self._btn2_cb)
        self.btn2.setGeometry(425, 10, 75, 40)
        self.btn2.setFont(font)
        self.btn3 = QtGui.QPushButton(u"沟通", self)
        self.btn3.setFlat(True)
        self.btn3.clicked.connect(self._btn3_cb)
        self.btn3.setGeometry(505, 10, 75, 40)
        self.btn3.setFont(font)
        self.btn4 = QtGui.QPushButton(u"成员", self)
        self.btn4.setFlat(True)
        self.btn4.clicked.connect(self._btn4_cb)
        self.btn4.setGeometry(585, 10, 75, 40)
        self.btn4.setFont(font)

        self.tbtn = QtGui.QToolButton(self)
        icon = QtGui.QIcon("plus.png")
        self.tbtn.setIcon(icon)
        self.tbtn.setIconSize(QtCore.QSize(24, 24))
        self.tbtn.clicked.connect(self._tbtn_cb)
        self.tbtn.move(950, 15)

    def _cbx_currentIndexChanged(self):
        #sys.exit(app.exec_())
        pass

    #INITBUG
    def _btn0_cb(self):
        self.state = INITBUG
        self.parent.convertState(self.state)

    # DYNAMIC
    def _btn1_cb(self):
        self.state = DYNAMIC
        self.parent.convertState(self.state)

    # SCHEDULE
    def _btn2_cb(self):
        self.state = SCHEDULE
        self.parent.convertState(self.state)

    # MESSAGE
    def _btn3_cb(self):
        self.state = MESSAGE
        self.parent.convertState(self.state)

    # MEMBER
    def _btn4_cb(self):
        self.state = MEMBER
        self.parent.convertState(self.state)

    # PLUS
    def _tbtn_cb(self):
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()
        painter.fillRect(rect, 'white')
        if self.state == DYNAMIC:
            painter.fillRect(345, 10, 75, 40, '#99ccff')
        elif self.state == SCHEDULE:
            painter.fillRect(425, 10, 75, 40, '#99ccff')
        elif self.state == MESSAGE:
            painter.fillRect(505, 10, 75, 40, '#99ccff')
        else:
            painter.fillRect(585, 10, 75, 40, '#99ccff')

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QtGui.QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


class Associate:
    def __init__(self, name):
        conn = sqlite3.connect(name+'.db')
        cu = conn.cursor()
        cu.execute("select name, phone, email from member where pid=10000")
        for row in cu:
            name, phone, email = row
        self.name = name
        self.phone = phone
        self.email = email
        self.master = ""

if __name__ == "__main__":
    ass = Associate("test")
    app = QtGui.QApplication(sys.argv)

    main = mainWindow(ass, MESSAGE)

    main.show_and_raise()
    sys.exit(app.exec_())

