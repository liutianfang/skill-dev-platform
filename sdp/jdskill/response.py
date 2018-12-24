class ResponseJD:
    response = None
    session = None
    intent = ""
    contexts = None
    directives = None
    shouldEndSession = False

    def __init__(self):
        self.session = {}
        self.contexts = {}
        self.response = {}
        self.directives = []

    def to_dict(self):
        response_dict = {}
        response_dict["version"] = "1.0"
        response_dict["intent"] = self.intent
        response_dict["contexts"] = self.contexts
        response_dict["directives"] = self.directives
        response_dict["shouldEndSession"] = self.shouldEndSession
        response_dict["response"] = self.response

        return response_dict

    def set_output_plantText(self, mesg=""):
        self.response["output"] = {"type": "PlainText", "text": mesg}

    def set_reprompt(self, mesg=""):
        self.response["reprompt"] = {"type": "PlainText", "text": mesg}


    def add_session_data(self, value, key="key"):
        self.contexts[key] = value

    def set_session_end(self):
        self.shouldEndSession = True