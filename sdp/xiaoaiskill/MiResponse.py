class MiResponse(object):
    version="1.0"
    session_attributes=None
    is_session_end=None
    response=None

    def __init__(self):
        self.version = "1.0"
        self.session_attributes = {}
        self. is_session_end = False
        self.response = {"open_mic": True}


    def to_dict(self):
        dict={}
        dict["version"]=self.version
        dict["is_session_end"]=self.is_session_end
        dict["session_attributes"]=self.session_attributes
        dict["response"]=self.response
        return dict

    def tts_text_out(self, content=""):
        self.response["to_speak"]={"type": 0, "text": content}

    def end_session(self):
        self.is_session_end=True

    def set_session_value(self, value, key="key"):
        self.session_attributes[key]=value

