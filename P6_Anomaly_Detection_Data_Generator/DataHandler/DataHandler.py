import os
import csv
import random
import sys
from urllib.request import DataHandler

import numpy as np

from DataHandler.Readings import Readings


class DataHandler:

    @staticmethod
    def RetrieveSensorReadings():
        listOfSensorReadings = []
        file = open('DataHandler/CityProbeData.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        # print(header)
        for row in csvreader:
            for num in range(20, len(row) - 1):
                if row[num] == '':
                    row[num] = float("nan")
                    print("x")
                row[num] = float(row[num])
            if all(float(i) < 15000 for i in row[20: len(row) - 1]):
                #listOfSensorReadings.append(row[0])
                listOfSensorReadings.append(row[20:len(row) - 1])

        # print(header[11:len(header) - 1])
        # for i in range(0, len(listOfSensorReadings) - 1):
        #        print(listOfSensorReadings[i])
        file.close()
        #return listOfSensorReadings
        return Readings(listOfSensorReadings, header[20:len(header) - 1])

    @staticmethod
    def RNGGenerator():
       randomNumber = random.choice(range(0,1599))
       return randomNumber

    @staticmethod
    def ProbabilityForAnomaly(probability):
        return random.random() < probability

    @staticmethod
    def generateAnomaly(readings, randomNumber): #number of colums we want anomalies in
        i = 0
        columns = []
        valueForHighDeviation = random.randint(0,1)
        valueforDirection = random.randint(0,1)
        numberOfFeaturesWithAnomalies = random.randint(0,6)

        while i < numberOfFeaturesWithAnomalies:
            num = random.randint(0, len(readings.headers) - 1)
            if not columns.__contains__(num):
                columns.append(num)
                i = i + 1

        for item in columns:
            std = readings.stdDeviations[item]
            maxVal = max(readings.yVals[item]) + std
            minVal = min(readings.yVals[item]) - std

            if valueForHighDeviation == 1:
                deviation = "high"
            else:
                deviation = "low"

            if valueforDirection == 1:
                direction = "up"
            else:
                direction = "down"

            if deviation == "high":
                if direction == "up":
                    value = random.uniform(maxVal + std, maxVal + 2 * std)
                else:
                    value = random.uniform(minVal - std, minVal - 2 * std)
            else:
                if direction == "up":
                    value = random.uniform(maxVal + 0.01, maxVal + std)
                else:
                    value = random.uniform(minVal - 0.01, minVal - std)

            readings.dataInRows[randomNumber][item] = round(value, 2)
        return readings.dataInRows[randomNumber]



