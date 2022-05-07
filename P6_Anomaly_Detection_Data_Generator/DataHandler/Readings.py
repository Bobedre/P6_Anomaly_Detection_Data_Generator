import numpy as np

class Readings:
    def __init__(self, rows, h):
        self.dataInRows = rows
        self.headers = h
        self.stdDeviations = []
        self.yVals = []
        self.xVals = []
        i = 0
        while i < len(self.headers):
            x, y = Readings.generateXandY(self.dataInRows, i)
            self.yVals.append(y)
            self.xVals.append(x)
            i = i + 1

        for item in self.yVals:
            self.stdDeviations.append(np.std(item))

    @staticmethod
    def generateXandY(rows, columnNum):
        x = []
        y = []
        i = 0
        for row in rows:
            if row[columnNum] == '':
                row[columnNum] = '0'
            y.append(float(row[columnNum]))
            i = i + 1
            x.append(i)
            # print(y)
        return x, y
