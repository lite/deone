# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from deone import Ui_MainWindow
import os
import simplejson
import sqlite3
import sys
import string
import xlrd

host = 'de-one.appspot.com'
#host = 'localhost:8080'
        

fn_uprev = 'data/uprev.json'
        
tables = {
    u"深成指399001.xls":"Market", 
    u"BJS交易类型2.xls":"Suggestion",
    u"DBS交易类型1.xls":"Suggestion",
    u"NRA交易类型4.xls":"Suggestion",
    u"SDB交易类型3.xls":"Suggestion",
    u"个股历史数据.xls":"StockHist",
    u"大盘数据.xls":"Market",
    u"StockCategory.xls":"StockCategory",
    u"CategoryHist.xls":"CategoryHist",
    }

from client import App3Client
c = App3Client('de-one.appspot.com', 'test', 'test')

class AdminWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(QtCore.QRect(0, 0, 320, 160))
        
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

        hLayoutTag = QtGui.QHBoxLayout()
        self.label_tag = QtGui.QLabel(self)
        hLayoutTag.addWidget(self.label_tag)
        self.lineEdit_tag = QtGui.QLineEdit(self)
        self.lineEdit_pass.setEchoMode(QtGui.QLineEdit.Password)
        hLayoutTag.addWidget(self.lineEdit_tag)
        mainLayout.addLayout(hLayoutTag)

        hLayoutCmd = QtGui.QHBoxLayout()
        self.pushButtonUpload = QtGui.QPushButton(self)
        hLayoutCmd.addWidget(self.pushButtonUpload)
        self.pushButtonReset = QtGui.QPushButton(self)
        hLayoutCmd.addWidget(self.pushButtonReset)
        self.pushButtonExit = QtGui.QPushButton(self)
        hLayoutCmd.addWidget(self.pushButtonExit)
        
        self.label_msg = QtGui.QLabel(self)
        self.label_msg.setGeometry(QtCore.QRect(0, 0, 320, 20))
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
        QtCore.QObject.connect(self.pushButtonUpload, QtCore.SIGNAL("pressed()"), self.doUpload)
        QtCore.QObject.connect(self.pushButtonReset, QtCore.SIGNAL("pressed()"), self.doReset)

        self.progbar.hide()
        self.center()
        
    def retranslateUi(self):
        self.label_user.setText(QtGui.QApplication.translate("MainWindow", "用户:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_pass.setText(QtGui.QApplication.translate("MainWindow", "密码:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_tag.setText(QtGui.QApplication.translate("MainWindow", "标记:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUpload.setText(QtGui.QApplication.translate("MainWindow", "上传", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonReset.setText(QtGui.QApplication.translate("MainWindow", "恢复", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonExit.setText(QtGui.QApplication.translate("MainWindow", "退出", None, QtGui.QApplication.UnicodeUTF8))
        
    def doExit(self):
        print("called doExit")
        self.close()
    
    def doReset(self):
        print("called doReset")
        usr=str(self.lineEdit_user.text())
        pwd=str(self.lineEdit_pass.text())
        tag=str(self.lineEdit_tag.text())
        if not self.reset(usr, pwd, tag):
            self.label_msg.setText("user can not reset.")
        
    def doUpload(self):
        print("called doUpload")
        usr=str(self.lineEdit_user.text())
        pwd=str(self.lineEdit_pass.text())
        tag=str(self.lineEdit_tag.text())
        if not self.upload(usr, pwd, tag):
            self.label_msg.setText("user can not upload.")
            
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        print(screen, size)
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) /2)

    def reset(self, usr, pwd, tag):
        from client import App3Client
        from datetime import datetime
        
        tm_begin = datetime.now()
        self.progbar.reset() 
        self.progbar.show()
        self.progbar.setRange(0, 100)
        self.label_msg.setText("resetting package...")
        c = App3Client(host, usr, pwd)
        
        items = {}
        if tag is None or len(tag) == 0:
            s = c.list('Deone')
            #print(s)
            if s is not None:
                items = simplejson.loads(s)
        else:
            root = simplejson.load(open(fn_uprev))
            if root is not None:
                if root.has_key(tag):
                    items = root[tag]
        prog_val = 1
        for item in items:
            id = item['id']
            self.label_msg.setText("reseting package %s...(%d/%d)" %(id, prog_val, len(items)))
            self.progbar.setValue(prog_val*100/len(items))
            s = c.delete('Deone', id)
            if s is None:
                ret = False
                break
            prog_val += 1
        
        ret = True
                
        tm_end = datetime.now()
        self.label_msg.setText("package reset completed. %d"%(tm_end - tm_begin).seconds)
        self.progbar.hide()
        return ret

    def upload(self, usr, pwd, tag):

        from client import App3Client
        from datetime import datetime
        
        tm_begin = datetime.now()

        self.progbar.reset() 
        self.progbar.show()
        self.progbar.setRange(0, 100)
        c = App3Client(host, usr, pwd)
        
        self.label_msg.setText("uploading package...")
        
        ret = True
        self.uprev_ids = []

        for fn,tbl in tables.items():
            if not self.xls2obj(c, fn, tbl):
                ret = False
                break
        
        #print(self.uprev_ids)
        local_root = {}
        if os.path.exists(fn_uprev):
            local_root = simplejson.load(open(fn_uprev))
            if local_root is not None:
                #print(local_root)
                if tag is None or len(tag) == 0:
                    tag = datetime.now().strftime("%Y-%m-%d")
        if local_root.has_key(tag):
            local_root[tag] += self.uprev_ids
        else:
            local_root[tag] = self.uprev_ids
        simplejson.dump(local_root, open(fn_uprev, 'w'))

        tm_end = datetime.now()
        self.label_msg.setText("package upload completed. %d"%(tm_end - tm_begin).seconds)
        self.progbar.hide()
        return ret

    def xls2obj(self, c, fn, tbl):
        wb = xlrd.open_workbook(os.path.join(os.path.abspath("data"), fn))
        sh = wb.sheet_by_index(0)

        #first line is columns
        cols = []
        for colnum in range(sh.ncols):
            t = sh.cell_type(0, colnum)
            val = sh.cell_value(0, colnum)
            cols +=[val]
        cells = []
        i_row = 0
        #sh.nrows = 5
        for rownum in xrange(1, sh.nrows):
            for colnum in range(sh.ncols):
                t = sh.cell_type(rownum, colnum)
                val = sh.cell_value(rownum, colnum)
                #print(rownum, colnum, t, val)
                if t == 3:
                    dt = xlrd.xldate_as_tuple(val, 0)
                    s_dt = "%04d-%02d-%02d"%(dt[0:3])
                    #print(s_dt)
                    cells += [s_dt]
                else:
                    try:
                        f = float(val)
                        i = int(f)
                        if  f == float(i):
                            cells += ["%d" %(i)]
                        else:
                            cells += ["%.2f" %(f)]
                    except ValueError:
                        cells += [val]
            i_row += 1
            
            #print(sh.nrows, rownum, i_row)
            self.label_msg.setText("uploading package %s...(%d/%d)" %(fn, rownum, sh.nrows))
            self.progbar.setValue(rownum*100/sh.nrows)
            
            if (i_row%5000==0) or (rownum == sh.nrows-1):
                obj = {"ncols":sh.ncols, "nrows":i_row+1, "cells":cols+cells}
                s_json = simplejson.dumps({tbl:obj})
                #print(s_json)
                s = c.post('Deone', {"data": s_json})
                #print(s)
                if s is None:
                    return False
                else:
                    obj = simplejson.loads(s)
                    if obj is not None:
                        self.uprev_ids += [{"id":obj["id"]}]
                cells = []
                i_row = 0
        
        return True
       
#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import os, sys
    if not os.path.exists('data'): os.mkdir('data')
    if os.path.exists('__local'):
        host = 'localhost:8080'
    app = QtGui.QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())