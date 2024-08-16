import os

from Sensibo_client.Sensibo_client import SensiboClientAPI

from PySide6.QtCore import QThread, Signal
from time import time, sleep
from random import randint

import json

class TemperatureControl(QThread):
    finished = Signal()
    signalUpdateOutputImage = Signal()
    signalStatusUpdate = Signal(str)
    signalExportImage = Signal(str)
    signalUpdateImageTitle = Signal(str)

    def __init__(self, T1, timeForT1, T2, timeForT2, timeStepMins, eachMeasurementTimePeriodMins, DaikinUID, SensiboAPIKey, parent = None):
        super(TemperatureControl, self).__init__(parent)
        #Copy the variables
        self.T1 = round(float(T1), 2)
        self.timeForT1 = timeForT1 * 60 #seconds
        self.T2 = round(float(T2), 2)
        self.timeForT2 = timeForT2 * 60 #seconds
        self.DaikinUID = DaikinUID
        self.SensiboAPIKey = SensiboAPIKey
        self.client = SensiboClientAPI(self.SensiboAPIKey)
        self.listTimeMin = []
        self.listCurrentTemperatureC = []
        self.measurementTimePeriodMins = eachMeasurementTimePeriodMins
        self.timeStepMins = timeStepMins
    
    def multipleModulations(self):
        totalNumbersOfMeasurements = int((self.timeForT1 + self.timeForT2)/(self.timeStepMins * 60))
    
        #Start the measurement
        for i in range(totalNumbersOfMeasurements):
            totalTime = self.timeForT1 + self.timeForT2
            newTimeForT1 = self.timeForT1 - (self.timeStepMins* 60 * i)
            newTimeForT2 = totalTime - newTimeForT1
            if (newTimeForT1 >= newTimeForT2):
                #Update the status
                self.signalStatusUpdate.emit("Start the measurement with {} C for {} mins and {} C for {} mins.\n".format(self.T1, round(newTimeForT1/60, 2), self.T2, round(newTimeForT2/60, 2)))
                self.signalUpdateImageTitle.emit("{} C for {} mins and {} C for {} mins".format(self.T1, round(newTimeForT1/60, 2), self.T2, round(newTimeForT2/60, 2)))
                self.temperatureModulation(newTimeForT1, newTimeForT2)
            
        #Finish the measurement
        self.stopMeasurement()
    
    def temperatureModulation(self, timeForT1, timeForT2):
        
        self.currentACState = self.client.pod_ac_state(self.DaikinUID)
        #Report the current status
        self.signalStatusUpdate.emit("-" * 10 + "Current AC state" + "-" *10 + "\n")
        self.signalStatusUpdate.emit(json.dumps(self.currentACState) + ".\n")

        #Get the current temperature
        ac_measurements = self.client.pod_measurement(self.DaikinUID)
        currentTemperature = round(float(ac_measurements[0]['temperature']), 2)
        #currentTimePeriodMin = 0
        #Report the current temperature
        self.signalStatusUpdate.emit("-" * 10 + "Measurement starts." + "-" *10 + "\n")

        #Start the modulation
        self.startTime = time()
        self.currentTimePeriodMin = round((time() - self.startTime)/60, 2)
        #Power on the ac
        self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "on", True)
        sleep(randint(1, 5))
        #Swing mode
        self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "swing", "rangeFull")
        sleep(randint(1, 5))
        self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "horizontalSwing", "rangeFull")
        sleep(randint(1, 5))
        #Change fan state
        self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "fanLevel", "medium_high")
        sleep(randint(1, 5))
        
        #Set the initial status where T = self.T2
        #self.T1 < self.T2
        #Case 1
        if (currentTemperature > self.T2) and (self.currentTimePeriodMin < self.measurementTimePeriodMins):
            #Report the current status
            self.signalStatusUpdate.emit("AC switched on. Cool the temperature to {} C.\n".format(self.T2))
            #Step 0, change the AC state to heat mode
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "mode", "cool")
            sleep(randint(1, 5))
            #Step 1, set the temperature to the T1 - 1
            initialSetTemperatureC = self.T1 - 1
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "targetTemperature", int(initialSetTemperatureC))
            sleep(randint(1, 5))

            while(currentTemperature > self.T2) and (self.currentTimePeriodMin < self.measurementTimePeriodMins):    
                #Wait 1 min and check the temperature again
                self.trusty_sleep(1*60)
                #Get the new temperature and current time period.
                ac_measurements = self.client.pod_measurement(self.DaikinUID)
                currentTemperature = round(float(ac_measurements[0]['temperature']), 2)
                self.currentTimePeriodMin = round((time() - self.startTime)/60, 2)
                #Report the current temperature 
                self.signalStatusUpdate.emit("Current temperature is {} C at {} minutes. Set temperature is {} C.\n".format(currentTemperature, self.currentTimePeriodMin, initialSetTemperatureC))
                self.signalStatusUpdate.emit("Will continue cooling the temperature to {} C before start cycling.\n".format(self.T2))
        
        #Case 2
        elif (currentTemperature < self.T2) and (self.currentTimePeriodMin < self.measurementTimePeriodMins): 
            #Report the current status
            self.signalStatusUpdate.emit("AC switched on. Heat the temperature to {} C.\n".format(self.T2))
            #Step 0, change the AC state to heat mode
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "mode", "heat")
            sleep(randint(1, 5))
            #Step 1, set the temperature to the T2 + 1
            initialSetTemperatureC = self.T2 + 1
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "targetTemperature", int(initialSetTemperatureC))
            sleep(randint(1, 5))

            while(currentTemperature < self.T2) and (self.currentTimePeriodMin < self.measurementTimePeriodMins):    
                #Wait 1 min and check the temperature again
                self.trusty_sleep(1*60)
                #Get the new temperature and current time period.
                ac_measurements = self.client.pod_measurement(self.DaikinUID)
                currentTemperature = round(float(ac_measurements[0]['temperature']), 2)
                self.currentTimePeriodMin = round((time() - self.startTime)/60, 2)
                #Report the current temperature 
                self.signalStatusUpdate.emit("Current temperature is {} C at {} minutes. Set temperature is {} C.\n".format(currentTemperature, self.currentTimePeriodMin, initialSetTemperatureC))
                self.signalStatusUpdate.emit("Will continue heating the temperature to {} C before start cycling.\n".format(self.T2))
        
        #Start temperature modulation
        #Update the status
        self.signalStatusUpdate.emit("Temperature reached {} C as the initial condition. Will start cycling the temperatures between {} and {}.\n".format(self.T2, self.T1, self.T2))
        numberOfCycles = 0

        #Step 2, alternate the temperautre between T1 and T2 at the chosen time period for each temperature for a user's input time interval.
        while (self.currentTimePeriodMin < self.measurementTimePeriodMins):
            #Step 1, set the temperature to the T1
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "mode", "cool")
            sleep(randint(1, 5))
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "targetTemperature", int(self.T1))
            #Stay here for the given time period 
            self.trusty_sleep(timeForT1)
            #Step 2, set the temperature to the T2
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "mode", "heat")
            sleep(randint(1, 5))
            self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "targetTemperature", int(self.T2))
            #Stay here for the given time period 
            self.trusty_sleep(timeForT2)
            #Get the current temperature and time.
            ac_measurements = self.client.pod_measurement(self.DaikinUID)
            currentTemperature = round(float(ac_measurements[0]['temperature']), 2)
            self.currentTimePeriodMin = round((time() - self.startTime)/60, 2)
            numberOfCycles += 1
            #Report the current temperature 
            self.signalStatusUpdate.emit("Finished {} cycles. Current temperature is {} C at {} minutes. \n".format(numberOfCycles, currentTemperature, self.currentTimePeriodMin))
        
        #Modulation finished. Update the status
        self.signalStatusUpdate.emit("Temperatur modulation finished. Exporting the image.\n")

        #Modulation finished. Send the signal for exporting the figure.
        self.signalExportImage.emit("{} C for {} mins and {} C for {} mins".format(self.T1, round(timeForT1/60, 2), self.T2, round(timeForT2/60, 2)))

    def stopMeasurement(self):
        #Switch off the AC
        self.client.pod_change_ac_state(self.DaikinUID, self.currentACState, "on", False)

        self.finished.emit()
    
    #Function to make sure the sleep function giving enough sleep time (seconds)
    def trusty_sleep(self, n):
        start = time()
        while(time() - start < n):
            sleep(n - (time()-start))