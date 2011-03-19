# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from ohlc import OHLCWidget
from querytable import QueryTableWidget

class TradingWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(QtGui.QWidget, self).__init__(parent)

        self.setObjectName("tabTrading")
        mainLayout = QtGui.QHBoxLayout()
        
        vLayoutOHLC = QtGui.QVBoxLayout()
        self.ohlc = OHLCWidget(self)
        self.ohlc.setObjectName("OHLCWidget")
        vLayoutOHLC.addWidget(self.ohlc)

        self.tblWidgetMarket = QueryTableWidget(self)
        self.tblWidgetMarket.setObjectName("tblWidgetMarket")
        vLayoutOHLC.addWidget(self.tblWidgetMarket)

        mainLayout.addLayout(vLayoutOHLC)

        vLayoutInfo = QtGui.QVBoxLayout()
        
        self.label_Title = QtGui.QLabel(self)
        vLayoutInfo.addWidget(self.label_Title)
        self.label_FX = QtGui.QLabel(self)
        vLayoutInfo.addWidget(self.label_FX)
        self.tblWidgetFX = QueryTableWidget(self)
        self.tblWidgetFX.setObjectName("tblWidgetFX")
        vLayoutInfo.addWidget(self.tblWidgetFX)

        self.label_JY = QtGui.QLabel(self)
        vLayoutInfo.addWidget(self.label_JY)
        self.tblWidgetJY = QueryTableWidget(self)
        self.tblWidgetJY.setObjectName("tblWidgetJY")
        vLayoutInfo.addWidget(self.tblWidgetJY)
        
        self.label_XX = QtGui.QLabel(self)
        vLayoutInfo.addWidget(self.label_XX)
        self.tblWidgetXX = QueryTableWidget(self)
        self.tblWidgetXX.setObjectName("tblWidgetXX")
        vLayoutInfo.addWidget(self.tblWidgetXX)
        
        self.label_ZS = QtGui.QLabel(self)
        vLayoutInfo.addWidget(self.label_ZS)
        self.tblWidgetZS = QueryTableWidget(self)
        self.tblWidgetZS.setObjectName("tblWidgetZS")
        vLayoutInfo.addWidget(self.tblWidgetZS)
        
        mainLayout.addLayout(vLayoutInfo)
        self.setLayout(mainLayout)

        self.retranslateUi()

        QtCore.QObject.connect(self.tblWidgetXX, QtCore.SIGNAL("selectionChanged()"), self.tblWidgetXX_selectionChanged)
        self.init()

    def retranslateUi(self):
        self.label_Title.setText(QtGui.QApplication.translate("MainWindow", "DeOne 量化策略交易模型", None, QtGui.QApplication.UnicodeUTF8))
        self.label_FX.setText(QtGui.QApplication.translate("MainWindow", "市场风险分析", None, QtGui.QApplication.UnicodeUTF8))
        self.label_JY.setText(QtGui.QApplication.translate("MainWindow", "交易数据", None, QtGui.QApplication.UnicodeUTF8))
        self.label_XX.setText(QtGui.QApplication.translate("MainWindow", "详细消息", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ZS.setText(QtGui.QApplication.translate("MainWindow", "操作指示", None, QtGui.QApplication.UnicodeUTF8))

    def tblWidgetXX_selectionChanged(self):
        print("call tblWidgetXX_selectionChanged")
        row=self.tblWidgetXX.currentRow()
        code = str(self.tblWidgetXX.item(row,0).text())
        print(code)
        #日期	股票代码	公司名称	开盘价格	最高价格	最低价格	收盘价格	成交量
        self.ohlc.query(u'select 日期,开盘价格,最高价格,最低价格,收盘价格,成交量 from StockHist where 股票代码=? order by 日期 asc'.encode('utf-8'), (code,))
        self.tblWidgetZS.query(u'select 日期,初始买入,最低买入,建仓价位,目标价位,最高目标,止损价位 from Suggestion where 股票代码=? and 日期=?'.encode('utf-8'), (code, self.date,))
        
    def init(self):
        self.date = '2009-07-10'
        #日期	市场代码	开盘	最高	最低	收盘	成交量	上涨个股	下跌个股	平盘个股	交易类型I	交易类型II 	交易类型III	交易类型IV	风险指标	动能指标
        self.tblWidgetMarket.query(u'select 日期,市场代码,开盘,最高,最低,收盘,成交量,上涨个股,下跌个股,平盘个股 from Market where 日期=?'.encode('utf-8'), (self.date,))
        self.tblWidgetFX.query(u'select 日期,市场代码,风险指标,动能指标 from Market where 日期=?'.encode('utf-8'), (self.date,))
        self.tblWidgetJY.query(u'select 日期,市场代码,交易类型I,交易类型II,交易类型III,交易类型IV from Market where 日期=?'.encode('utf-8'), (self.date,))
        #日期	股票代码	公司名称	交易类型	初始买入	最低买入	建仓价位	目标价位	最高目标	止损价位
        self.tblWidgetXX.query(u'select 股票代码,公司名称,交易类型 from Suggestion where 日期=?'.encode('utf-8'), (self.date,))
        
#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QMainWindow, QApplication
    
    class ApplicationWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.widget = TradingWidget(self)
            self.widget.setFocus()
            self.setCentralWidget(self.widget)
           
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())