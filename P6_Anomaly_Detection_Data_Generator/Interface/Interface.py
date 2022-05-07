import json
import logging
import time

from P6_Anomaly_Detection_Data_Generator.DataGenerator.DataGenerator import DataGenerator
from signalrcore.hub_connection_builder import HubConnectionBuilder

class Interface:

    def connectToHub(self):
        self.hub_connection = HubConnectionBuilder()\
            .with_url("http://localhost:8081/suggestorHub")\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                })\
            .configure_logging(logging.DEBUG)\
            .build()
        self.hub_connection.on_open(lambda: self.onConnection())
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.on("GeneratorStart", self.GenerateData())
        self.hub_connection.start()

        while not self.end:
            time.sleep(1)

        self.hub_connection.stop()

    def onConnection(self):
        print("connection opened and handshake received ready to send messages")
        self.hub_connection.send("GeneratorJoin", [])


    def GenerateData(self):
        dataGenerator = DataGenerator()
        while True:
            result = dataGenerator.generateData()
            self.sendResultToHub(result)


    def sendResultToHub(self, result):
        json_dump = json.dumps(result)
        self.hub_connection.send("ProbeReading", json_dump)
        print("result send")
