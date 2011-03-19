# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, Qt
from matplotlibwidget import MatplotlibWidget

import sqlite3
import datetime

class QueryTableWidget(QtGui.QTableWidget):
    def __init__(self, parent):
        super(QtGui.QTableWidget, self).__init__(parent)
        self.setObjectName("DBTableWidget")
        
        self.horizontalHeader().setStretchLastSection(True)
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.setShowGrid(True)
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(20)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setResizeMode(Qt.QHeaderView.Fixed)
        #self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setMouseTracking(True)
        #self.setEnabled(False)
        
    def keyPressEvent(self, event) :
        print("keyPressEvent")
        #print(event.modifiers(), event.key())
        if event.modifiers() == Qt.Qt.AltModifier :
            if event.key() == Qt.Qt.Key_Up :
                print("alt+up")
            elif event.key() == Qt.Qt.Key_Down :
                print("alt+down")
        else :
            Qt.QTableWidget.keyPressEvent(self, event)

    def mousePressEvent(self, event):
        print("mousePressEvent")
        if event.button() == Qt.Qt.LeftButton and self.indexAt(event.pos()).row() > -1 :
            print(event.button, self.indexAt(event.pos()).row())
        Qt.QTableWidget.mousePressEvent(self, event)

    def selectionChanged(self, new, old):
        print("selectionChanged", new, old)
        #row=self.currentRow()
        #col=self.currentColumn()
        #print(self.item(row,0).text())
        #print(self.item(row,2).text())
        self.emit(QtCore.SIGNAL("selectionChanged()"))
        Qt.QTableWidget.selectionChanged(self, new, old)

    def query(self, sql, parameters=None):
        self.clear()

        # select data from sqlite3 db
        deone_db = r'data/DEONE.db'
        con = sqlite3.connect(deone_db)
        con.text_factory=str
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        #t = u'深发展Ａ'.encode('utf-8')
        #cur.execute(u'select * from StockHist where 股票名称=?'.encode('utf-8'), (t,))
        #cur.execute('select * from StockHist')
        cur.execute(sql, parameters)

        irow = 0
        ncols = 0
        for irow in xrange(100):
            row = cur.fetchone()
            if row == None:
                break
            #print(row)
            ncols = len(row)
            if irow == 0:
                self.setColumnCount(ncols)
                #self.setStretchLastSection(True)

                for ind in xrange(ncols):
                    s = row.keys()[ind].decode('utf-8')
                    item = QtGui.QTableWidgetItem(s)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    self.setHorizontalHeaderItem(ind, item)
            self.insertRow(irow)
            for icol in xrange(ncols):
                s = row[icol].decode('utf-8')
                item = QtGui.QTableWidgetItem(s)
                #item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                item.setWhatsThis("You can change this task's comment, start time and end time.");
                self.setItem(irow,icol,item);  
        con.close()
        self.setRowCount(irow)   
        
        # Sorting columns
        for col in range(ncols):
            self.resizeColumnToContents(col)
        self.setCurrentItem(self.item(0,0))
        
#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QMainWindow, QApplication
    
    class ApplicationWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.tblwidget = QueryTableWidget(self)
            self.tblwidget.setFocus()
            self.setCentralWidget(self.tblwidget)
            
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())