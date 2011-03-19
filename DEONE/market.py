# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from ohlc import OHLCWidget
from querytable import QueryTableWidget

class MarketWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(QtGui.QWidget, self).__init__(parent)

        self.setObjectName("tabMarket")

        mainLayout = QtGui.QVBoxLayout()
        
        hLayoutQuery = QtGui.QHBoxLayout()
        self.pushButtonMarketSH = QtGui.QPushButton(self)
        #self.pushButtonMarketSH.setGeometry(QtCore.QRect(50, 5, 75, 23))
        self.pushButtonMarketSH.setObjectName("pushButtonMarketSH")
        hLayoutQuery.addWidget(self.pushButtonMarketSH)

        self.pushButtonMarketSZ = QtGui.QPushButton(self)
        #self.pushButtonMarketSZ.setGeometry(QtCore.QRect(200, 5, 75, 23))
        self.pushButtonMarketSZ.setObjectName("pushButtonMarketSZ")
        hLayoutQuery.addWidget(self.pushButtonMarketSZ)

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

        QtCore.QObject.connect(self.pushButtonMarketSH, QtCore.SIGNAL("pressed()"), self.doQueryMarketSH)
        QtCore.QObject.connect(self.pushButtonMarketSZ, QtCore.SIGNAL("pressed()"), self.doQueryMarketSZ)

        self.doQueryMarketSH()

    def retranslateUi(self):
        self.pushButtonMarketSZ.setText(QtGui.QApplication.translate("MainWindow", "深证成指", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonMarketSH.setText(QtGui.QApplication.translate("MainWindow", "上证指数", None, QtGui.QApplication.UnicodeUTF8))
        
    def doQueryMarketSH(self):
        print("called doQueryMarketSH")
        self.doQueryMarket('999999')
        
    def doQueryMarketSZ(self):
        print("called doQueryMarketSH")
        self.doQueryMarket('399001')

    def doQueryMarket(self, code):
        #日期	市场代码	开盘	最高	最低	收盘	成交量	上涨个股	下跌个股	平盘个股	交易类型I	交易类型II 	交易类型III	交易类型IV	风险指标	动能指标
        self.ohlc.query(u'select 日期,开盘,最高,最低,收盘,成交量 from Market where 市场代码=? order by 日期 asc'.encode('utf-8'), (code,))
        self.tbl.query(u'select * from Market where 市场代码=? order by 日期 desc'.encode('utf-8'), (code,))
        
#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QMainWindow, QApplication
    
    class ApplicationWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.widget = MarketWidget(self)
            self.widget.setFocus()
            self.setCentralWidget(self.widget)
           
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())