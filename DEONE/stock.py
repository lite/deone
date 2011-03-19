# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ohlc import OHLCWidget
from querytable import QueryTableWidget

class StockWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(QtGui.QWidget, self).__init__(parent)
        self.setObjectName("tabStock")
        
        mainLayout = QtGui.QVBoxLayout()
        
        hLayoutQuery = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 10, 46, 14))
        self.label.setObjectName("label")
        hLayoutQuery.addWidget(self.label)

        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(80, 0, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        hLayoutQuery.addWidget(self.lineEdit)

        self.pushButtonQuery = QtGui.QPushButton(self)
        self.pushButtonQuery.setGeometry(QtCore.QRect(210, 0, 75, 23))
        self.pushButtonQuery.setObjectName("pushButtonQuery")
        hLayoutQuery.addWidget(self.pushButtonQuery)

        mainLayout.addLayout(hLayoutQuery)

        hLayoutInfo = QtGui.QHBoxLayout()
        
        self.ohlc = OHLCWidget(self)
        self.ohlc.setObjectName("OHLCWidget")
        hLayoutInfo.addWidget(self.ohlc)

        self.tbl = QueryTableWidget(self)
        self.tbl.setObjectName("QueryTableWidget")
        hLayoutInfo.addWidget(self.tbl)

        mainLayout.addLayout(hLayoutInfo)
        self.setLayout(mainLayout)

        self.retranslateUi()

        QtCore.QObject.connect(self.pushButtonQuery, QtCore.SIGNAL("pressed()"), self.doQuery)

        self.lineEdit.setText('1')
        self.doQuery()

    def retranslateUi(self):
        self.label.setText(QtGui.QApplication.translate("MainWindow", "股票代码", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonQuery.setText(QtGui.QApplication.translate("MainWindow", "查询", None, QtGui.QApplication.UnicodeUTF8))
        
    def doQuery(self):
        print("called doQuery")
        code = str(self.lineEdit.text())
        #日期	股票代码	公司名称	开盘价格	最高价格	最低价格	收盘价格	成交量
        self.ohlc.query(u'select 日期,开盘价格,最高价格,最低价格,收盘价格,成交量 from StockHist where 股票代码=? order by 日期 asc'.encode('utf-8'), (code,))
        self.tbl.query(u'select * from StockHist where 股票代码=? order by 日期 desc'.encode('utf-8'), (code,))
        pass

#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QMainWindow, QApplication
    
    class ApplicationWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.tblwidget = StockWidget(self)
            self.tblwidget.setFocus()
            self.setCentralWidget(self.tblwidget)
           
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())