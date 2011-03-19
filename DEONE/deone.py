# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DEONE.ui'
#
# Created: Mon Aug 02 09:11:58 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import deone_rc

from trading import TradingWidget
from sector import SectorWidget
from stock import StockWidget
from market import MarketWidget

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        
        self.setObjectName("MainWindow")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setDocumentMode(False)
        
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionStock = QtGui.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/image/icons/log.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStock.setIcon(icon)
        self.actionStock.setObjectName("actionStock")
        self.actionSector = QtGui.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/image/icons/misc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSector.setIcon(icon1)
        self.actionSector.setObjectName("actionSector")
        self.actionTrading = QtGui.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/image/icons/kchart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTrading.setIcon(icon2)
        self.actionTrading.setObjectName("actionTrading")
        self.actionMarket = QtGui.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/image/icons/terminal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMarket.setIcon(icon3)
        self.actionMarket.setObjectName("actionMarket")
        self.actionQuit = QtGui.QAction(self)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/image/icons/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon5)
        self.actionQuit.setObjectName("actionQuit")
        self.menuView.addAction(self.actionTrading)
        self.menuView.addAction(self.actionStock)
        self.menuView.addAction(self.actionSector)
        self.menuView.addAction(self.actionMarket)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionQuit)
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionTrading)
        self.toolBar.addAction(self.actionStock)
        self.toolBar.addAction(self.actionSector)
        self.toolBar.addAction(self.actionMarket)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionQuit)
        
        self.connect(self.actionTrading, QtCore.SIGNAL("triggered()"), self.doTabTrading)
        self.connect(self.actionStock, QtCore.SIGNAL("triggered()"), self.doTabStock)
        self.connect(self.actionSector, QtCore.SIGNAL("triggered()"), self.doTabSector)
        self.connect(self.actionMarket, QtCore.SIGNAL("triggered()"), self.doTabMarket)
        self.connect(self.actionQuit, QtCore.SIGNAL("triggered()"), self.doQuit)

        self.tabWidget = QtGui.QTabWidget(self)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        
        self.tabTrading = TradingWidget(self.tabWidget)
        self.tabWidget.addTab(self.tabTrading, "")

        self.tabSector = SectorWidget(self.tabWidget)
        self.tabWidget.addTab(self.tabSector, "")

        self.tabStock = StockWidget(self.tabWidget)
        self.tabWidget.addTab(self.tabStock, "")

        self.tabMarket = MarketWidget(self.tabWidget)
        self.tabWidget.addTab(self.tabMarket, "")
        self.tabWidget.setCurrentIndex(0)
        
        self.setCentralWidget(self.tabWidget)
    
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DEONE", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "功能", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "工具条", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStock.setText(QtGui.QApplication.translate("MainWindow", "股票", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSector.setText(QtGui.QApplication.translate("MainWindow", "板块", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTrading.setText(QtGui.QApplication.translate("MainWindow", "交易", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMarket.setText(QtGui.QApplication.translate("MainWindow", "大盘", None, QtGui.QApplication.UnicodeUTF8))
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTrading), QtGui.QApplication.translate("MainWindow", "交易", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSector), QtGui.QApplication.translate("MainWindow", "板块", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStock), QtGui.QApplication.translate("MainWindow", "股票", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMarket), QtGui.QApplication.translate("MainWindow", "大盘", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "退出", None, QtGui.QApplication.UnicodeUTF8))
        
    def doTabTrading(self):
        print("called doTabTrading")
        self.tabWidget.setCurrentIndex(1)

    def doTabStock(self):
        print("called doTabStock")
        self.tabWidget.setCurrentIndex(2)

    def doTabSector(self):
        print("called doTabSector")
        self.tabWidget.setCurrentIndex(3)

    def doTabMarket(self):
        print("called doTabMarket")
        self.tabWidget.setCurrentIndex(4)

    def doQuit(self):
        print("called doQuit")
        self.close()

#===============================================================================
#   Example
#===============================================================================
if __name__ == "__main__":
    import sys
    
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec_())
