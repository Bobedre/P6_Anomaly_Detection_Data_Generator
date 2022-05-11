class Interface:
    clients = {}
    hub_connection = None
    end = False

    def __init__(self):
        self.connectToHub()

    def connectToHub(self):
        self.hub_connection = HubConnectionBuilder() \
            .with_url("http://localhost:8081/suggestorHub") \
            .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
        }) \
            .configure_logging(logging.DEBUG) \
            .build()
        self.hub_connection.on_open(lambda: self.onConnection())
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.on("JoinGroup", self.clientConnect)
        self.hub_connection.on("LeaveGroup", self.clientDisconnect)
        self.hub_connection.on("suggestionRequest", self.sendSuggestions)
        self.hub_connection.on("evaluateSentence", self.evaluateSentence)
        self.hub_connection.on("test", print)
        self.hub_connection.start()

        while not self.end:
            time.sleep(1)

        self.hub_connection.stop()

    def onConnection(self):
        print("connection opened and handshake received ready to send messages")
        self.hub_connection.send("SuggesterJoin", [])

    def clientConnect(self, groupID):
        self.clients[groupID[0]] = Client(groupID[0])
        print("Client has joined with id")
        print(groupID)

    def clientDisconnect(self, groupID):
        del self.clients[groupID[0]]
        print("Client with id")
        print(groupID)
        print("Has disconnected")

    def sendSuggestions(self, inputs):
        json_load = json.loads(inputs[1])
        if not (inputs[0] in self.clients.keys()):
            self.clientConnect([inputs[0]])
        suggestions = self.clients[inputs[0]].autocompleter.run_auto_completer(json_load["Sentence"],
                                                                               json_load["MaxResults"])
        sugesstionsJson = SuggestionJson(suggestions)
        json_dump = json.dumps(sugesstionsJson.__dict__, ensure_ascii=False)
        self.hub_connection.send("SendGroupMessage", [inputs[0], "suggestionResponse", json_dump])

    def evaluateSentence(self, inputs):
        sentence = inputs[0]
        print("Evaluating sentence")
        RelevanceEvaluator().evaluateQuery(sentence)
