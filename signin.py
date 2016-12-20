# -*- coding:utf-8 -*-

import sys
import webbrowser
from PySide import QtCore, QtGui


class Signin(QtGui.QMainWindow):
    def __init__(self):
        super(Signin, self).__init__()

        x, y, w, h = 500, 200, 400, 300
        self.setGeometry(x, y, w, h)
        self.setFixedSize(QtCore.QSize(400, 300))

        account_label = QtGui.QLabel("Cellphone No./Fetion No./E-Mail:", self)
        x, y, w, h = 40, 40, 221, 30
        account_label.setGeometry(x, y, w, h)

        self.account_combox = QtGui.QComboBox(self)
        self.account_combox.setEditable(True)
        self.account_combox.setGeometry(70, 70, 200, 26)
        self.connect(self.account_combox, QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self._account_combox_currentIndexChanged)

        passwd_label = QtGui.QLabel("Password:", self)
        passwd_label.setGeometry(40, 110, 62, 30)

        self.passwd_lineedit = QtGui.QLineEdit(self)
        self.passwd_lineedit.setGeometry(70, 140, 200, 22)
        self.passwd_lineedit.setEchoMode(QtGui.QLineEdit.Password)

        reset_passwd_label = QtGui.QLabel("tips", self)
        reset_passwd_label.setGeometry(300, 140, 130, 30)
        reset_passwd_tips = 'CMCC user could send "p" to 12520 to reset password'
        reset_passwd_label.setToolTip(reset_passwd_tips)

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
            self.passwd_lineedit.setText("")

    def _clear_btn_cb(self):
        self.account_combox.clearEditText()
        self.passwd_lineedit.setText("")

    def _signin_btn_cb(self):
        self.username = self.account_combox.currentText()
        self.passwd = self.passwd_lineedit.text()




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    demo = Signin()
    demo.show()

    sys.exit(app.exec_())
