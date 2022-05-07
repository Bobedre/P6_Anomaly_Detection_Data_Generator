import random
import time

from  P6_Anomaly_Detection_Data_Generator.DataHandler.DataHandler import DataHandler

class DataGenerator:

    def generateData(self):
        reading = DataGenerator.generateReadings()
        sleepTime = random.randint(3,10)
        print(sleepTime)
        time.sleep(sleepTime)
        return reading

    @staticmethod
    def generateReadings():
        readings = DataHandler.RetrieveSensorReadings()
        indexForReading = DataHandler.RNGGenerator()
        probability = DataHandler.ProbabilityForAnomaly(0.05)

        if probability == True:
            readingWithAnomaly = DataHandler.generateAnomaly(readings, indexForReading)
            #print("anomaly:")
            #print(readingWithAnomaly)
            return readingWithAnomaly
        else :
            #print("non anomaly:")
            #print(readings.dataInRows[indexForReading])
            return readings.dataInRows[indexForReading]
