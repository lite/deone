# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from deone import Ui_MainWindow
import os
import simplejson
import sqlite3

host = 'de-one.appspot.com'
#host = 'localhost:8080'

deone_db = 'data/DEONE.db'

tables = ["Market", "Suggestion", "StockHist", "StockCategory", "CategoryHist",]

class LoginWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(QtCore.QRect(0, 0, 200, 120))
        
        mainLayout = QtGui.QVBoxLayout()
        
        hLayoutUser = QtGui.QHBoxLayout()
        self.label_user = QtGui.QLabel(self)
        hLayoutUser.addWidget(self.label_user)
        self.lineEdit_user = QtGui.QLineEdit(self)
        self.lineEdit_user.setText("test")
        hLayoutUser.addWidget(self.lineEdit_user)
        mainLayout.addLayout(hLayoutUser)

        hLayoutPass = QtGui.QHBoxLayout()
        self.label_pass = QtGui.QLabel(self)
        hLayoutPass.addWidget(self.label_pass)
        self.lineEdit_pass = QtGui.QLineEdit(self)
        self.lineEdit_pass.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_pass.setText("test")
        hLayoutPass.addWidget(self.lineEdit_pass)
        mainLayout.addLayout(hLayoutPass)

        hLayoutCmd = QtGui.QHBoxLayout()
        self.pushButtonLogin = QtGui.QPushButton(self)
        hLayoutCmd.addWidget(self.pushButtonLogin)
        self.pushButtonExit = QtGui.QPushButton(self)
        hLayoutCmd.addWidget(self.pushButtonExit)
        
        self.label_msg = QtGui.QLabel(self)
        mainLayout.addWidget(self.label_msg)
        
        self.progbar = QtGui.QProgressBar(self) 
        self.progbar.setProperty("value",QtCore.QVariant(0)) 
        mainLayout.addWidget(self.progbar)
        
        mainLayout.addLayout(hLayoutCmd)

        widget = QtGui.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        
        self.retranslateUi()
        QtCore.QObject.connect(self.pushButtonExit, QtCore.SIGNAL("pressed()"), self.doExit)
        QtCore.QObject.connect(self.pushButtonLogin, QtCore.SIGNAL("pressed()"), self.doLogin)

        self.progbar.hide()
        self.center()
        
    def retranslateUi(self):
        self.label_user.setText(QtGui.QApplication.translate("MainWindow", "用户:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_pass.setText(QtGui.QApplication.translate("MainWindow", "密码:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLogin.setText(QtGui.QApplication.translate("MainWindow", "登入", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonExit.setText(QtGui.QApplication.translate("MainWindow", "退出", None, QtGui.QApplication.UnicodeUTF8))
        
    def doExit(self):
        print("called doExit")
        self.close()
    
    def doLogin(self):
        print("called doLogin")
        usr=str(self.lineEdit_user.text())
        pwd=str(self.lineEdit_pass.text())
        if self.update(usr, pwd):
            self.showDeone()
        else:
            self.label_msg.setText("user can not login.")
            
    def showDeone(self):
        self.main = Ui_MainWindow()
        self.main.showFullScreen()
        self.main.show()
        self.close()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        print(screen, size)
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) /2)

    def update(self, usr, pwd):
        print(usr, pwd)
        #1. get the version
        from client import App3Client
        from datetime import datetime
        
        tm_begin = datetime.now()

        fn_rev = 'data/rev.json' 
        self.progbar.reset() 
        self.progbar.show()
        self.progbar.setRange(0, 100)
        self.label_msg.setText("checking the latest version...")
        c = App3Client(host, usr, pwd)
        # 1. list all packages
        s = c.list('Deone')
        if s is None:
            ret = False
        else:
            # get local packages
            local_items = []
            if os.path.exists(fn_rev):
                local_v = simplejson.load(open(fn_rev))
                for local_item in local_v:
                    local_items += [local_item['id']]
                
            #3. get deone package
            self.label_msg.setText("updating package...")
            prog_val = 1
            v = simplejson.loads(s)
            for item in v:
                id = item['id']
                if id not in local_items:
                    self.label_msg.setText("updating package %s...(%d/%d)" %(id, prog_val, len(v)))
                    self.progbar.setValue(prog_val*100/len(v))
                    s = c.get('Deone', id)
                    prog_val += 1
                    if s is not None:
                        root = simplejson.loads(s)
                        #admin.json2sqlite3(root["data"] )
                        self.json2sqlite3(root["data"] )
            #4. update local version
            simplejson.dump(v, open(fn_rev, 'w'))
            ret = True
        tm_end = datetime.now()
        self.label_msg.setText("package update completed. %d"%(tm_end - tm_begin).seconds)
        self.progbar.hide()
        return ret

    def json2sqlite3(self, str):
        con = sqlite3.connect(deone_db)
        obj = simplejson.loads(str)
        for tbl in tables:
            if obj.has_key(tbl):
                self.obj2table(con, tbl, obj[tbl])
        con.close()

    def obj2table(self, con, tbl, obj):
        cur = con.cursor()
        ncols = obj["ncols"]
        nrows = obj["nrows"]
        cells = obj["cells"]
        #print(ncols, nrows, cells)
        for rownum in range(nrows):
            t = []
            for colnum in range(ncols):
                #print(rownum, colnum)
                idx = rownum*ncols + colnum
                t += [cells[idx]]
                #print(idx, cells[idx])
            if rownum == 0:
                s_cols = ""
                for s_col in t:
                    s_cols += s_col + " text,"
                s = '''create table %s(%s)'''%(tbl, s_cols.rstrip(','))
                try:
                    cur.execute(s)
                    con.commit()
                except sqlite3.OperationalError, e:
                    print(e) 
            else:
                s_cols = ("?,"*ncols)
                s = '''insert into %s values (%s)'''%(tbl, s_cols.rstrip(','))
                #print(s)
                cur.execute(s, t)
        con.commit()
        cur.close()

#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import os, sys
    if not os.path.exists('data'): os.mkdir('data')
    if os.path.exists('__local'):
        host = 'localhost:8080'
    app = QtGui.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())