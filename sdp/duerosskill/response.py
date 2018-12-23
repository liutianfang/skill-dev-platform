
class ResponseDUEROS:
    response = {}
    session = {"attributes": {}}
    contexts = {}

    def __init__(self):
        self.response["shouldEndSession"] = False

    def to_dict(self):
        responseTemp = {}
        responseTemp["version"] = "2.0"
        responseTemp["contexts"] = self.contexts
        responseTemp["session"] = self.session
        responseTemp["response"] = self.response

        return responseTemp

    '''
    设置文本输出
    '''

    def tts_output(self, mesg=""):
        self.response["outputSpeech"] = {"type": "PlainText", "text": mesg}

    '''
    设置session传递的数据
    '''


    def add_session_data(self,  key:str,value):
        self.session["attributes"][key] = value
    '''
    设置对话结束
    '''

    def set_session_end(self):
        self.response["shouldEndSession"] = True