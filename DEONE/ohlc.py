# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from matplotlib.pyplot import setp
from matplotlib.ticker import Formatter
from matplotlib.dates import YearLocator, MonthLocator, WeekdayLocator, DayLocator, DateFormatter, drange, MONDAY, num2date, date2num

import sqlite3
import datetime

class OHLCWidget(Canvas):
    def __init__(self, parent=None):
        from matplotlib import rcParams
        rcParams['font.size'] = 6

        self.figure = Figure(facecolor='w',edgecolor='w')
        self.figure.subplots_adjust(left=0.1, right=0.9, wspace=0.6)
        
        Canvas.__init__(self, self.figure)
        self.setParent(parent)
        self.figure.canvas.mpl_connect('motion_notify_event', self.onmove)
        
        Canvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        return QtCore.QSize(10, 10)

    def onmove(self, event):
        if event.xdata == None or event.inaxes == self.info_axes:
            return
        #print(event.x, event.xdata, event.inaxes)
        ind = int(round(event.xdata))
        self.info(ind)

    def info(self, ind):
        print("call info", ind)
        if ind>=len(self.rows) or ind<0: return ''
        row = self.rows[ind]
        if row == None:
            return
        print(row)
        #today = datetime.datetime(1899,12,30)+datetime.timedelta(days=float(row[0]))
        y,m,d = row[0].split('-')
        today = datetime.datetime(int(y), int(m), int(d))
        open = float(row[1])
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        volume= int(float(row[5])) 
        print(today, open, high, low, close, volume)

        self.info_axes.clear()
        self.info_axes.text(0.1, 0.95, 'Date')
        self.info_axes.text(0.15, 0.93, today.strftime("%Y%m%d"), color='b')
        self.info_axes.text(0.1, 0.90, 'Open')
        self.info_axes.text(0.15, 0.88, open, color='b')
        self.info_axes.text(0.1, 0.85, 'High')
        self.info_axes.text(0.15, 0.83, high, color='b')
        self.info_axes.text(0.1, 0.80, 'Low')
        self.info_axes.text(0.15, 0.78, low, color='b')
        self.info_axes.text(0.1, 0.75, 'Close')
        self.info_axes.text(0.15, 0.73, close, color='b')
        self.info_axes.text(0.1, 0.70, 'Volume')
        self.info_axes.text(0.15, 0.68, volume, color='b')
        self.info_axes.set_xticklabels([])
        self.info_axes.set_yticklabels([])

        self.figure.canvas.draw()
    
    def query(self, sql, parameters=None):
        self.figure.clear()

        self.vol_axes = self.figure.add_axes([0.06, 0.01, 0.87, 0.24], axisbg='#cccccc', autoscale_on=True)
        self.ohlc_axes = self.figure.add_axes([0.06, 0.25, 0.87, 0.74], axisbg='#cccccc', autoscale_on=True)
        self.info_axes = self.figure.add_axes([0.93, 0.01, 0.06, 0.98], axisbg='#cccccc', autoscale_on=True)

        # select data from sqlite3 db
        deone_db = r'data/DEONE.db'
        con = sqlite3.connect(deone_db)
        con.text_factory=str
        cur = con.cursor()
        #t = u'深发展Ａ'.encode('utf-8')
        #cur.execute(u'select * from StockHist where 股票名称=?'.encode('utf-8'), (t,))
        #cur.execute('select * from StockHist')
        cur.execute(sql, parameters)
        
        dates = []
        ind = 0
        self.rows = []
        for ind in xrange(100):
            row = cur.fetchone()
            if row == None:
                break
            #print(row)
            self.rows += [row]

            #today = datetime.datetime(1899,12,30)+datetime.timedelta(days=float(row[0]))
            y,m,d = row[0].split('-')
            today = datetime.datetime(int(y), int(m), int(d))
            dates += [today]
            open = float(row[1])
            high = float(row[2])
            low = float(row[3])
            close = float(row[4])
            volume= int(float(row[5])) 
            #print(ind, today, open, high, low, close, volume)

            if close>open:
                col = "r"
            elif close<open:
                col = "g"
            else:
                col = "w"
                self.ohlc_axes.hlines(open, ind-0.3, ind+0.3, colors='w')
               
            self.ohlc_axes.bar(ind, close-open, 0.6, open, color=col, align='center')
            self.ohlc_axes.vlines(ind, low, high, color=col)
            self.vol_axes.bar(ind, volume, 0.6, color=col, align='center')
       
        con.close()

        formatter = MyFormatter(dates)
        self.ohlc_axes.xaxis.set_major_formatter(formatter)
        self.vol_axes.xaxis.set_major_formatter(formatter)
       
        self.ohlc_axes.set_xlim(-0.5, ind+1.5)
        self.ohlc_axes.grid(True)
        self.vol_axes.set_xlim(-0.5, ind+1.5)
        self.vol_axes.grid(True)

        self.vol_axes.set_xticklabels([])
        self.info_axes.set_xticklabels([])
        self.info_axes.set_yticklabels([])

        self.figure.autofmt_xdate()

        self.info(ind-1)
        
class MyFormatter(Formatter):
    def __init__(self, dates, fmt='%Y %b %d'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        ind = int(round(x))
        if ind>=len(self.dates) or ind<0: return ''
        s = self.dates[ind].strftime(self.fmt)
        #print(x, ind, s) 
        return s

#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QMainWindow, QApplication
    
    class ApplicationWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.ohlc = OHLCWidget(self)
            self.ohlc.setFocus()
            self.setCentralWidget(self.ohlc)
            code ='1.0'
            self.ohlc.query(u'select 日期,开盘,最高,最低,收盘,成交量 from StockHist where 股票代码=?'.encode('utf-8'), (code,))
        
    
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())