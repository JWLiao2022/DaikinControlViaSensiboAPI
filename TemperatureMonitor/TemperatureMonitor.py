from Sensibo_client.Sensibo_client import SensiboClientAPI

from PySide6.QtCore import QThread, Signal
from time import time, sleep

import json

class TemperatureMonitor(QThread):
    finished = Signal()
    signalUpdateOutputImage = Signal()
    signalStatusUpdate = Signal(str)
    
    def __init__(self, DaikinUID, SensiboAPIKey, parent = None):
        super(TemperatureMonitor, self).__init__(parent)
        #Initialise parameters
        self.DaikinUID = DaikinUID
        self.SensiboAPIKey = SensiboAPIKey
        self.client = SensiboClientAPI(self.SensiboAPIKey)
        self.listTimeMin = []
        self.listCurrentTemperatureC = []
        self.isContinueUpdating = True
        self.updateTimePeriodMin = 1.0 #mins
        self.numberOfMeasurements = 0
    
    def startMonitoring(self):
        #Start monitoring
        #Update the plot every mins
        while self.isContinueUpdating:
            #Append the very first point
            if self.numberOfMeasurements == 0:
                self.refleshingDataSet()
            
            self.numberOfMeasurements += 1

            self.trusty_sleep(self.updateTimePeriodMin * 60)

            currentTimePeriodMin = round((time() - self.startTime)/60, 2)
            ac_measurements = self.client.pod_measurement(self.DaikinUID)
            currentHumidity = round(float(ac_measurements[0]['humidity']), 2)
            currentTemperatureC = round(float(ac_measurements[0]['temperature']), 2)
            #Update the time and temperature lists for plotting
            self.listTimeMin.append(currentTimePeriodMin)
            self.listCurrentTemperatureC.append(currentTemperatureC)
            self.signalUpdateOutputImage.emit()
            self.signalStatusUpdate.emit("Current temperature is {} C at time of {} mins, and current humidity is {} %.\n".format(currentTemperatureC, currentTimePeriodMin, currentHumidity))

    def refleshingDataSet(self):
        
        #Update the status
        self.signalStatusUpdate.emit("Refreshing the measurment plot.\n")
        
        self.listTimeMin = []
        self.listCurrentTemperatureC = []
        self.startTime = time()
        ac_measurements = self.client.pod_measurement(self.DaikinUID)
        currentTimePeriodMin = 0
        currentTemperatureC = round(float(ac_measurements[0]['temperature']), 2)
        currentHumidity = round(float(ac_measurements[0]['humidity']), 2)
        
        self.listTimeMin.append(currentTimePeriodMin)
        self.listCurrentTemperatureC.append(currentTemperatureC)
        self.signalUpdateOutputImage.emit()
        self.signalStatusUpdate.emit("Current temperature is {} C at time of {} mins, and current humidity is {} %.\n".format(currentTemperatureC, currentTimePeriodMin, currentHumidity))

    def stopUpdating(self):
        self.finished.emit()

    #Function to make sure the sleep function giving enough sleep time (seconds)
    def trusty_sleep(self, n):
        start = time()
        while(time() - start < n):
            sleep(n - (time()-start))
