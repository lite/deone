# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from querytable import QueryTableWidget

class SectorWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(QtGui.QWidget, self).__init__(parent)

        self.setObjectName("tabSector")

        mainLayout = QtGui.QHBoxLayout()
        
        vLayoutLeft = QtGui.QVBoxLayout()
        self.label_DX = QtGui.QLabel(self)
        vLayoutLeft.addWidget(self.label_DX)

        hLayoutQuery = QtGui.QHBoxLayout()
        self.label_RQ = QtGui.QLabel(self)
        hLayoutQuery.addWidget(self.label_RQ)

        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(80, 0, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        hLayoutQuery.addWidget(self.lineEdit)

        self.pushButtonQuery = QtGui.QPushButton(self)
        self.pushButtonQuery.setGeometry(QtCore.QRect(210, 0, 75, 23))
        self.pushButtonQuery.setObjectName("pushButtonQuery")
        hLayoutQuery.addWidget(self.pushButtonQuery)
    
        vLayoutLeft.addLayout(hLayoutQuery)
        
        self.tblWidgetBK = QueryTableWidget(self)
        self.tblWidgetBK.setObjectName("tblWidgetBK")
        vLayoutLeft.addWidget(self.tblWidgetBK)

        mainLayout.addLayout(vLayoutLeft)

        vLayoutRight = QtGui.QVBoxLayout()
        self.label_GG = QtGui.QLabel(self)
        vLayoutRight.addWidget(self.label_GG)
        self.tblWidgetGG = QueryTableWidget(self)
        self.tblWidgetGG.setObjectName("tblWidgetGG")
        vLayoutRight.addWidget(self.tblWidgetGG)

        self.label_ZS = QtGui.QLabel(self)
        vLayoutRight.addWidget(self.label_ZS)
        self.tblWidgetZS = QueryTableWidget(self)
        self.tblWidgetZS.setObjectName("tblWidgetZS")
        vLayoutRight.addWidget(self.tblWidgetZS) 
        
        mainLayout.addLayout(vLayoutRight)

        self.setLayout(mainLayout)

        self.retranslateUi()

        QtCore.QObject.connect(self.pushButtonQuery, QtCore.SIGNAL("pressed()"), self.doQuery)
        #self.emit(QtCore.SIGNAL("selectionChanged()"))
        QtCore.QObject.connect(self.tblWidgetBK, QtCore.SIGNAL("selectionChanged()"), self.tblWidgetBK_selectionChanged)
        QtCore.QObject.connect(self.tblWidgetGG, QtCore.SIGNAL("selectionChanged()"), self.tblWidgetGG_selectionChanged)


        self.lineEdit.setText('2009-07-10')
        self.doQuery()

    def retranslateUi(self):
        self.label_DX.setText(QtGui.QApplication.translate("MainWindow", "板块动向", None, QtGui.QApplication.UnicodeUTF8))
        self.label_RQ.setText(QtGui.QApplication.translate("MainWindow", "交易日期", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonQuery.setText(QtGui.QApplication.translate("MainWindow", "查询", None, QtGui.QApplication.UnicodeUTF8))
        self.label_GG.setText(QtGui.QApplication.translate("MainWindow", "板块个股", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ZS.setText(QtGui.QApplication.translate("MainWindow", "操作指示", None, QtGui.QApplication.UnicodeUTF8))
        
    def doQuery(self):
        print("called doQuery")
        date = str(self.lineEdit.text())
        #self.tblWidgetBK.query(u'select * from CategoryHist where 股票代码=?'.encode('utf-8'), (date,))
        self.tblWidgetBK.query(u'select * from CategoryHist'.encode('utf-8'), ())
        pass

    def tblWidgetBK_selectionChanged(self):
        print("called tblWidgetBK_selectionChanged")
        row=self.tblWidgetBK.currentRow()
        code = str(self.tblWidgetBK.item(row,0).text())
        print(code)
        #select * from StockHist where 股票代码 in (select 股票代码 from StockCategory where 板块代码='YH') 
        self.tblWidgetGG.query(u'select * from StockHist where 股票代码 in (select 股票代码 from StockCategory where 板块代码=?) order by 日期 desc'.encode('utf-8'), (code,))
        
    def tblWidgetGG_selectionChanged(self):
        print("called tblWidgetGG_selectionChanged")
        row=self.tblWidgetGG.currentRow()
        code = str(self.tblWidgetGG.item(row,2).text())
        print(code)
        self.tblWidgetZS.query(u'select * from Suggestion where 股票代码=? order by 日期 desc'.encode('utf-8'), (code,))
        
#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QMainWindow, QApplication
    
    class ApplicationWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.widget = SectorWidget(self)
            self.widget.setFocus()
            self.setCentralWidget(self.widget)
           
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())