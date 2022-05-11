import random
import time

from DataHandler.DataHandler import DataHandler

class DataGenerator:

    @staticmethod
    def generateData():
        reading = DataGenerator.generateReadings()
        sleepTime = 3#random.randint(3,10)
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
