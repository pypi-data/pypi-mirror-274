import os
import csv
import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPixmap, QIcon, QPen, QPalette, QBrush, QAction
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QGroupBox, QComboBox, QPushButton
from PySide6.QtWidgets import QLabel, QRadioButton, QCheckBox, QLineEdit 
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
import qwt

from smon.sampling import SamplingThread


XNODE_CODE="""
import time
from pop.core  import Uart
from pop.ext import IMU

imu = IMU()

imu.init()
    
while True:
    w, x, y, z = imu.read(IMU.QUATERNION)
    data = "{},{},{},{},".format(w, x, y, z)
    x, y, z = imu.read(IMU.ACCELERATION)
    data += "{},{},{},".format(x, y, z)
    x, y, z = imu.read(IMU.GYROSCOPE) 
    data += "{},{},{},".format(x, y, z)
    x, y, z = imu.read(IMU.MAGNETIC)
    data += "{},{},{},".format(x, y, z)
    x, y, z = imu.read(IMU.EULER)
    data += "{},{},{}".format(x, y, z)
    
    Uart.write(data, slip=True)
"""

ABOUT = "Version: 1.0.0\n\nPySide6: 6.6.2\nPythonQwt: 0.12.1\n\n©PlanX Labs. 2024"

class Oscilloscope(QMainWindow):
    PLOT_X_INIT_MAX = 8

    changeCurveSignal = Signal(int, bool)
    resetSignal = Signal()
    closeSignal = Signal()
    
    def __init__(self, group, iport, mcast, clipboard, log_name):
        super().__init__()
        
        self.samplingThread = SamplingThread(self, group, iport, mcast, log_name)
        self.samplingThread.samplingSignal.connect(self.onDraw)
        self.samplingThread.changeUiSignal.connect(self.onChangeUI)        
        self.samplingThread.changeChannelLenSignal.connect(self.onChangeChannelLen)
        self.samplingThread.start()
        self.clipboard = clipboard
        self.__log_name = log_name
        
        self.initGUI()
                  
    def closeEvent(self, event):
        self.closeSignal.emit()

    def resizeEvent(self, event):  
        self.resizeTable()
           
    def onReset(self):
        self.resetSignal.emit()
        
        for i in range(self.channelLen): 
            self.curves[i].setSamples([0], [0])
        
        self.tbDatas.clearContents()
        self.tbDatas.setRowCount(0)
        
        self.btSaveData.setEnabled(False)

    def onStopStart(self):        
        if self.btStopStart.text() == "Stop":
            self.btStopStart.setText("Start")
            self.isWait = True
            if self.tbDatas.rowCount():
                self.btSaveData.setEnabled(True)
        else:
            self.btStopStart.setText("Stop")
            self.isWait = False
            self.btSaveData.setEnabled(False)
        
    def onChangeUI(self, enable):
        if enable:
            self.enableUI()
        else:
            self.disableUI()
    
    def onChangeChannelLen(self, n):
        self.channelLen = n
        self.onReset()
           
    def onChCurve(self, index):
        stat = (self.chCurves[index].checkState() == Qt.CheckState.Checked)
        
        if stat:
            self.curves[index].setPen(self.pens[index])
            self.iRawCurves |= 1 << index
        else:
            self.curves[index].setPen(QPen(Qt.GlobalColor.darkGray, 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            self.iRawCurves &= ~(1 << index)

        if self.iRawCurves == 0:
            self.chCurvesSelect.setCheckState(Qt.CheckState.Unchecked)
        elif self.iRawCurves == 2 ** self.channelLen  - 1:
            self.chCurvesSelect.setCheckState(Qt.CheckState.Checked)
        else:
            self.chCurvesSelect.setCheckState(Qt.CheckState.PartiallyChecked)

        self.changeCurveSignal.emit(index, stat)

    def onChCurveSelect(self, _):
        stat = self.chCurvesSelect.checkState()
       
        if stat == Qt.CheckState.PartiallyChecked:
            self.chCurvesSelect.setCheckState(Qt.CheckState.Checked)
            
        for i in range(self.channelLen):
            self.chCurves[i].setChecked(stat == Qt.CheckState.Checked or stat == Qt.CheckState.PartiallyChecked)
            self.onChCurve(i)
        
    def onRbAuto(self):
        self.leMin.setEnabled(False)
        self.leMax.setEnabled(False)
        self.btManualOk.setEnabled(False)
        
        self.plot.setAxisAutoScale(qwt.QwtPlot.yLeft)
                
    def onRbManual(self):
        self.leMin.setEnabled(True)
        self.leMax.setEnabled(True)
        self.btManualOk.setEnabled(True)
        
    def onBtManualOk(self):
        try:
            min = float(self.leMin.text())
            max = float(self.leMax.text())
        except ValueError:
            return
        
        self.plot.setAxisScale(qwt.QwtPlot.yLeft, min, max)
    
    def onCurveStyle(self):
        for i in range(self.channelLen):
            self.curves[i].setStyle(self.cbCurveStyle.currentIndex())
                
    def onPlotBgColor(self):
        self.plot.setCanvasBackground(self.plotBgColors[self.cbPlotBgColor.currentText()])
    
    def onCurveWidth(self):
        w = int(self.cbCurveWidth.currentText())
        self.pens = [QPen(c, w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin) for c in self.colors]
        
        for i in range(self.channelLen):
            if self.chCurves[i].checkState() == Qt.CheckState.Checked:
                self.curves[i].setPen(self.pens[i])
    
    def onSaveData(self):
        fname = QFileDialog.getSaveFileName(self, filter='CSV (*.csv)')[0]
        if not fname:
            return
        
        column_len = self.channelLen
        
        line = ['Data' + str(i) for i in range(column_len)]
        line.insert(0, 'Time')
        column_len += 1
        
        with open(fname, 'w+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(line)
                    
            for row in range(self.tbDatas.rowCount()):
                for column in range(column_len):
                    item = self.tbDatas.item(row, column)
                    if item:
                        d = item.text()
                    else:
                        d = '0'
                    line[column] = d
                writer.writerow(line)

    def onXnodeCode(self):
        msgbox = QMessageBox(self)        
        msgbox.setIconPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "smon_xnode_code.png")))
        msgbox.setWindowTitle("The code below needs to be run on XNode.")
        copy_bt = msgbox.addButton("Copy", QMessageBox.ButtonRole.YesRole)
        copy_bt.clicked.connect(lambda : self.clipboard.setText(XNODE_CODE))
        msgbox.addButton("Ok", QMessageBox.ButtonRole.YesRole)        
        msgbox.exec()

    def __setTwItem(self, row, column, data):
        item = QTableWidgetItem(str(data))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setForeground(QColor(90,90,90))
        item.setBackground(QColor(250,250,250))
        
        self.tbDatas.setItem(row, column, item)
    
    def __setTableData(self, t, data):               
        row = self.tbDatas.rowCount()
        self.tbDatas.insertRow(row)
        
        self.__setTwItem(row, 0, t)        
        
        for i in range(self.channelLen): 
            self.__setTwItem(row, i+1, data[i])
        
        self.tbDatas.selectRow(row)
        
    def onDraw(self, samples):
        if self.isWait: return
                
        x_time = samples[0:1, :].reshape(SamplingThread.SAMPLE_RANGE)
        y_data = samples[1:, :]
                
        for i in range(self.channelLen): 
            self.curves[i].setSamples(qwt.QwtPointArrayData(x_time, y_data[i], len(x_time)))
            
        self.plot.setAxisScale(qwt.QwtPlot.xBottom, x_time[0], max(self.PLOT_X_INIT_MAX, x_time[-1]), 0.5)
        self.plot.replot()
       
        self.__setTableData(x_time[-1], y_data[:, -1:].reshape(self.channelLen))
        
    def initGUI(self):          
        self.setWindowTitle("Oscilloscope")
        self.resize(1280, 800)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "smon.png")))
        
        self.initMenuStatusBar()

        header = self.initHeader()
        body = self.initBody()
                
        central = QWidget()
        centralInner = QVBoxLayout()
        centralInner.addWidget(header)
        centralInner.addWidget(body)
        central.setLayout(centralInner)
        self.setCentralWidget(central)
        
        self.channelLen = 0
        self.iRawCurves = 0
        self.onRbAuto()
    
    def initHeader(self):
        self.colors = [QColor(name) for name in [
            'deeppink', 'hotpink', 'lightpink',
            'dodgerblue', 'deepskyblue', 'lightskyblue', 
            'forestgreen', 'lime', 'greenyellow', 
            'orange', 'gold', 'yellow',
            'darkmagenta', 'darkorchid', 'magenta', 'violet',] 
        ]

        self.pens = [QPen(c, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin) for c in self.colors ]
             
        header = QGroupBox("Configuration")
        headerInner = QGridLayout()
        
        headerInner00 = QWidget()
        headerInner10 = QWidget()
        
        headerInnerChCurve = self.initHeaderInnerChCurve()
        headerInnerOption = self.initHeaderInnerOption()
        
        headerInner00.setLayout(headerInnerChCurve)
        headerInner10.setLayout(headerInnerOption)

        headerInner.addWidget(headerInner00, 0, 0)
        headerInner.addWidget(headerInner10, 1, 0)
                       
        header.setLayout(headerInner)
        
        return header

    def initHeaderInnerChCurve(self):
        headerInnerChCurve = QHBoxLayout()
        
        self.chCurves = [None] * (SamplingThread.MAX_CHANNEL + 1)

        for i in range(SamplingThread.MAX_CHANNEL):
            self.chCurves[i] = self.initChCurve("D"+str(i), self.colors[i], self.onChCurve, i)
            headerInnerChCurve.addWidget(self.chCurves[i])

        self.chCurvesSelect = self.initChCurve("ALL", Qt.GlobalColor.darkGray, self.onChCurveSelect, -1)
        self.chCurvesSelect.setTristate(True) 
        headerInnerChCurve.addWidget(self.chCurvesSelect)
        
        return headerInnerChCurve
    
    def initHeaderInnerOption(self):
        headerInnerOption = QHBoxLayout()

        rbAuto = QRadioButton('Auto')
        rbAuto.clicked.connect(self.onRbAuto)
        rbAuto.setChecked(True)
        rbManual = QRadioButton('Manual')
        rbManual.clicked.connect(self.onRbManual)
        
        self.leMin = QLineEdit()
        self.leMin.setText('-10')
        self.leMin.setFixedWidth(50)
        self.leMax = QLineEdit()
        self.leMax.setText('10')
        self.leMax.setFixedWidth(50)
        
        self.btManualOk = QPushButton('Ok')
        self.btManualOk.clicked.connect(self.onBtManualOk)
        self.cbCurveStyle = QComboBox()
        self.cbCurveStyle.addItems(['Lines', 'Sticks', 'Steps', 'Dots'])
        self.cbCurveStyle.currentIndexChanged.connect(self.onCurveStyle)
        
        self.plotBgColors = {'Whitesmoke':QBrush(QColor('Whitesmoke')), 
                             'Lightgray':QBrush(QColor('Lightgray')), 
                             'Indigo':QBrush(QColor('Indigo')), 
                             'Midnightblue':QBrush(QColor('Midnightblue')), 
                             'Darkslategray':QBrush(QColor('Darkslategray')), 
                             'Black':QBrush(QColor('Black'))}
        
        self.cbPlotBgColor = QComboBox()
        self.cbPlotBgColor.addItems(list(self.plotBgColors))
        self.cbPlotBgColor.setCurrentIndex(4)
        self.cbPlotBgColor.currentIndexChanged.connect(self.onPlotBgColor)
        self.cbCurveWidth = QComboBox()
        self.cbCurveWidth.addItems(['2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.cbCurveWidth.setFixedWidth(50)
        self.cbCurveWidth.currentIndexChanged.connect(self.onCurveWidth)
        
        self.btSaveData = QPushButton('Save As')
        self.btSaveData.setEnabled(False)
        self.btSaveData.clicked.connect(self.onSaveData)
        self.btReset = QPushButton("Reset")
        self.btReset.clicked.connect(self.onReset)
        self.btReset.setEnabled(False)
        
        self.btStopStart = QPushButton("Stop")
        self.btStopStart.clicked.connect(self.onStopStart)
        self.btStopStart.setEnabled(False)
        
        headerInnerOption.addStretch(1)
        headerInnerOption.addWidget(rbAuto)
        headerInnerOption.addWidget(rbManual)
        headerInnerOption.addWidget(self.leMin)
        headerInnerOption.addWidget(QLabel('~'))
        headerInnerOption.addWidget(self.leMax)
        headerInnerOption.addWidget(self.btManualOk)
        headerInnerOption.addStretch(1)
        headerInnerOption.addWidget(QLabel('Style'))
        headerInnerOption.addWidget(self.cbCurveStyle)
        headerInnerOption.addWidget(QLabel('BgColor'))
        headerInnerOption.addWidget(self.cbPlotBgColor)
        headerInnerOption.addWidget(QLabel('Width'))
        headerInnerOption.addWidget(self.cbCurveWidth)        
        headerInnerOption.addStretch(2)
        headerInnerOption.addWidget(self.btSaveData)
        headerInnerOption.addWidget(self.btReset)
        headerInnerOption.addWidget(self.btStopStart)        
        headerInnerOption.addStretch(1)
        
        return headerInnerOption

    def initBody(self):
        body = QGroupBox('Plot') 
        self.bodyInner = QVBoxLayout()        
        self.initPlot()       
        self.initTable()          
        body.setLayout(self.bodyInner)
                        
        return body        
                
    def initPlot(self):
        self.plot = qwt.QwtPlot()

        grid = qwt.QwtPlotGrid()
        grid.setMajorPen(QPen(Qt.GlobalColor.darkGray, 0, Qt.PenStyle.DotLine))
        grid.attach(self.plot)
        
        self.plot.setCanvasBackground(QBrush(QColor('Darkslategray')))
        self.plot.setAxisTitle(qwt.QwtPlot.xBottom, 'Time')
        self.plot.setAxisScale(qwt.QwtPlot.xBottom, 0, self.PLOT_X_INIT_MAX, 0.5)
        self.plot.setAxisTitle(qwt.QwtPlot.yLeft, 'Value')
        self.plot.setAxisAutoScale(qwt.QwtPlot.yLeft)
                
        self.curves = [qwt.QwtPlotCurve() for _ in range(SamplingThread.MAX_CHANNEL)]

        for i in range(SamplingThread.MAX_CHANNEL):
            self.curves[i].setRenderHint(qwt.QwtPlotItem.RenderAntialiased)
            self.curves[i].setPen(self.pens[i])
            self.curves[i].setStyle(qwt.QwtPlotCurve.Lines)
            self.curves[i].attach(self.plot)

        self.bodyInner.addWidget(self.plot)

    def initTable(self):
        lbHeader = ['Time']
        lbHeader += ['D' + str(i) for i in range(SamplingThread.MAX_CHANNEL)]
        
        self.tbDatas = QTableWidget()
        self.tbDatas.setColumnCount(SamplingThread.MAX_CHANNEL+1)
        self.tbDatas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tbDatas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbDatas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbDatas.setHorizontalHeaderLabels(lbHeader)
        self.tbDatas.setFixedHeight(185)
        self.tbDatas.setMinimumWidth(1280)
        
        self.bodyInner.addWidget(self.tbDatas)
        self.resizeTable()
            
    def initMenuStatusBar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        help_menu = menubar.addMenu("&Help")
    
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(QApplication.quit)
        
        xnode_code_action = QAction("XNode &Code", self)
        xnode_code_action.triggered.connect(self.onXnodeCode)        
        about_action = QAction("&About", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "Oscilloscope", ABOUT))
        
        file_menu.addAction(exit_action)
        help_menu.addAction(xnode_code_action)
        help_menu.addAction(about_action)
       
        self.sbText = QLabel('Idle')
        self.statusBar().addWidget(self.sbText, 1)
        
    def initChCurve(self, label, color, connect_fn, connect_param):
        checkBox = QCheckBox(label, self)
        checkBox.setChecked(False)
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, color)
        checkBox.setPalette(p)
        checkBox.clicked.connect(lambda: connect_fn(connect_param))
        checkBox.setEnabled(False)
        
        return checkBox

    def resizeTable(self):
        header = self.tbDatas.horizontalHeader()
        wfactor = self.tbDatas.width() // header.count() - 1

        for column in range(header.count()):
            header.resizeSection(column, wfactor)

    def disableUI(self):       
        for i in range(self.channelLen):
            self.chCurves[i].setChecked(False)
            self.chCurves[i].setEnabled(False)
        
        self.chCurvesSelect.setCheckState(Qt.CheckState.Unchecked)
        self.chCurvesSelect.setEnabled(False)
        self.iRawCurves = 0
            
        self.btReset.setEnabled(False)
        self.btStopStart.setEnabled(False)
        self.btStopStart.setText("Stop")
                
        if self.tbDatas.rowCount():
            self.btSaveData.setEnabled(True)
        
        self.sbText.setText('Idle')
                
    def enableUI(self):        
        for i in range(self.channelLen):
            self.chCurves[i].setChecked(True)
            self.chCurves[i].setEnabled(True)
        
        self.chCurvesSelect.setEnabled(True)
        self.chCurvesSelect.setCheckState(Qt.CheckState.Checked)
        self.iRawCurves = 2 ** self.channelLen - 1
                                   
        self.btReset.setEnabled(True)
        self.btStopStart.setEnabled(True)
        
        self.btSaveData.setEnabled(False)
        
        self.plot.setAxisScale(qwt.QwtPlot.xBottom, 0, self.PLOT_X_INIT_MAX, 0.5)
        for i in range(self.channelLen):
            self.curves[i].setPen(self.pens[i])
            self.curves[i].setSamples([0], [0])

        self.sbText.setText('Running')        
        
        self.isWait = False
