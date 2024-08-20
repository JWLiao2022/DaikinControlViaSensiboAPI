import sys
import os

from Sensibo_client.Sensibo_client import SensiboClientAPI
from PySide6.QtCore import QThread, Slot, QPoint
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from DaikinControlUI.ui_form import Ui_Widget
from TemperatureControl.TemperatureControl import TemperatureControl
from TemperatureMonitor.TemperatureMonitor import TemperatureMonitor

import argparse
import json

import pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph.Qt import QtGui

from time import time

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Initiallise global parameters
        self.deviceName = ""
        self.APIKey = ""
        self.T1degreeC = 0.0
        self.T1TimePeriodMins = 0.0
        self.T2degreeC = 0.0
        self.T2TimePeriodMins = 0.0
        self.timeStepSizeMins = 0.0
        self.timePeriodForEachMeasurementMins = 0.0
        #UI
        self.qPointAnchor = QPoint(0,0)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.pushButtonInitialCheck.clicked.connect(self.checkAvailableDaikinDevices)
        self.ui.pushButton_StartMeasurement.clicked.connect(self.startMeasurement)
        self.ui.pushButton_StopMeasurement.clicked.connect(self.stopMeasurement)
        self.ui.pushButton_StopMeasurement.setEnabled(False)
        self.plotInitialser()

    def checkAvailableDaikinDevices(self):
        self.APIKey = self.ui.lineEditAPIKey.text()
        client = SensiboClientAPI(self.APIKey)
        self.dictDevices = client.devices()
        self.firstDeviceName = next(iter(self.dictDevices))
        self.DaikinUID = self.dictDevices[self.firstDeviceName]
        #Report the available devices
        self.qtSlot_StatusReport(json.dumps(self.dictDevices) + '\n')
        #Set the first device as the default device for the measurement
        self.ui.lineEdit_DeviceName.setText(self.firstDeviceName)
    
    def startMeasurement(self):
        #Copy the user input file
        self.T1degreeC = float(self.ui.lineEdit_T1.text())
        self.T1TimePeriodMins = float(self.ui.lineEdit_T1PeriodMins.text())
        self.T2degreeC = float(self.ui.lineEdit_T2.text())
        self.T2TimePeriodMins = float(self.ui.lineEdit_T2PeriodMins.text())
        self.timeStepSizeMins = float(self.ui.lineEdit_TimeStepSizeMins.text())
        self.timePeriodForEachMeasurementMins = float(self.ui.lineEdit_MeasurementTimePeriodMins.text())

        #Ask for the folder for the output result
        self.dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select directory",
            os.getcwd(),
            options=QFileDialog.Option.DontUseNativeDialog,
            )
        #Change the forward slash to the backward slash
        self.dir_path = os.path.normpath(self.dir_path)

        self.newMeasurement = TemperatureControl(self.T1degreeC, self.T1TimePeriodMins, self.T2degreeC, self.T2TimePeriodMins, self.timeStepSizeMins, self.timePeriodForEachMeasurementMins, 
                                                 self.DaikinUID, self.APIKey)
        self.newTemperatureMonitoring = TemperatureMonitor(self.DaikinUID, self.APIKey)
        
        #Start a new thread
        self.thread = QThread(self)
        #Move the process to the thread
        self.newMeasurement.moveToThread(self.thread)
        #Connect signals with slots
        self.thread.started.connect(self.newMeasurement.multipleModulations)
        self.newMeasurement.finished.connect(self.thread.quit)
        self.newMeasurement.finished.connect(self.newMeasurement.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.newMeasurement.signalStatusUpdate.connect(self.qtSlot_StatusReport)
        self.newMeasurement.signalExportImage.connect(self.qtSlot_ExportImage)
        self.newMeasurement.signalUpdateImageTitle.connect(self.qtSlot_UpdateImageTitle)
        self.newMeasurement.finished.connect(self.qtSlot_StopUpdatingPlot)
        #self.newMeasurement.signalUpdateOutputImage.connect(self.qtSlot_UpdatePlot)

        #Second thread for updating the temperature plot
        self.threadTemperaturePlot = QThread(self)
        self.newTemperatureMonitoring.moveToThread(self.threadTemperaturePlot)
        self.threadTemperaturePlot.started.connect(self.newTemperatureMonitoring.startMonitoring)
        self.newTemperatureMonitoring.finished.connect(self.threadTemperaturePlot.quit)
        self.newTemperatureMonitoring.finished.connect(self.newTemperatureMonitoring.deleteLater)
        self.threadTemperaturePlot.finished.connect(self.threadTemperaturePlot.deleteLater)
        self.newTemperatureMonitoring.signalUpdateOutputImage.connect(self.qtSlot_UpdatePlot)
        self.newTemperatureMonitoring.signalStatusUpdate.connect(self.qtSlot_StatusReport)

        #Start the measurement
        self.thread.start()
        self.threadTemperaturePlot.start()
        
        #Set the UI after starting a measurement
        self.ui.pushButton_StartMeasurement.setEnabled(False)
        self.ui.pushButton_StopMeasurement.setEnabled(True)
        
    def stopMeasurement(self):
        #Stop the current running measurment
        self.newMeasurement.stopMeasurement()
        self.newTemperatureMonitoring.stopUpdating()
        #Reset the UI bottons
        self.ui.pushButton_StartMeasurement.setEnabled(True)
        self.ui.pushButton_StopMeasurement.setEnabled(False)

    def plotInitialser(self):
        
        self.ui.graphicsViewTemperaturePlot.setTitle("Time dependent temperature variation.")
        self.ui.graphicsViewTemperaturePlot.showAxis('right')
        self.ui.graphicsViewTemperaturePlot.showAxis('top')
        self.ui.graphicsViewTemperaturePlot.setLabel(axis='left', text='Temperature (C)')
        self.ui.graphicsViewTemperaturePlot.setLabel(axis='bottom', text='Time (min)')
        self.ui.graphicsViewTemperaturePlot.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.graphicsViewTemperaturePlot.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.graphicsViewTemperaturePlot.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.graphicsViewTemperaturePlot.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.graphicsViewTemperaturePlot.showGrid(True, True)
        self.ui.graphicsViewTemperaturePlot.setYRange(23.4, 26.2, padding=0.05)
    
    @Slot()
    def qtSlot_StatusReport(self, txtStatusUpdate):
        #Report the avaliable devices
        self.ui.textEditStatusUpdate.insertPlainText(txtStatusUpdate)
        #Anchor the vertical scroll bar to the bottom
        vsb = self.ui.textEditStatusUpdate.verticalScrollBar()
        vsb.setValue(vsb.maximum())
    
    @Slot()
    def qtSlot_UpdatePlot(self):
        #Plot the updated results.
        #Reset the plot first
        self.ui.graphicsViewTemperaturePlot.clear()
        self.ui.graphicsViewTemperaturePlot.plot(self.newTemperatureMonitoring.listTimeMin, self.newTemperatureMonitoring.listCurrentTemperatureC, symbol = 's', symbolSize = 10,
                                                 symbolBrush=(255, 255, 0), symbolPen=(255, 255, 0))
    
    @Slot()
    def qtSlot_ExportImage(self, outputFileName):
        finaloutputFileName = outputFileName + ".png"

        full_output_file_path = os.path.join(self.dir_path, finaloutputFileName)
        #Export the plot
        #Update the status
        self.ui.textEditStatusUpdate.insertPlainText("Save the plot to {}.\n".format(full_output_file_path))
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.graphicsViewTemperaturePlot.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(full_output_file_path)
        #Clear the plot and reset the plot data set
        #self.newTemperatureMonitoring.refleshingDataSet()
        self.newTemperatureMonitoring.numberOfMeasurements = 0
        self.newMeasurement.startTime = time()
        self.ui.graphicsViewTemperaturePlot.clear()
    
    @Slot()
    def qtSlot_UpdateImageTitle(self, currentCycleParameters):
        self.ui.graphicsViewTemperaturePlot.setTitle(currentCycleParameters)
    
    @Slot()
    def qtSlot_StopUpdatingPlot(self):

        while self.newTemperatureMonitoring.isContinueUpdating:
            self.newTemperatureMonitoring.isContinueUpdating = False

        self.newTemperatureMonitoring.stopUpdating()
        #Reset the UI bottons
        self.ui.pushButton_StartMeasurement.setEnabled(True)
        self.ui.pushButton_StopMeasurement.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())
