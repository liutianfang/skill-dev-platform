from botskill.models import *
import random, datetime

MY_NAME = "应用唤醒词"
START_MSG = "你好，我是" + MY_NAME

HELP_MSG = "帮助信息"
AGAIN_MSG = "我没有听明白，再说一次吧"
EXIT_MSG = "再见"
GAME_STAET_MSG = "游戏开始"


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

    def setPlantText(self, mesg=""):
        self.response["outputSpeech"] = {"type": "PlainText", "text": mesg}

    '''
    设置session传递的数据
    '''

    def add_session_data(self, value, key="key"):
        self.session["attributes"][key] = value

    '''
    设置对话结束
    '''

    def set_session_end(self):
        self.response["shouldEndSession"] = True


class Processer(object):
    request = {}
    response = None
    request_type = ""
    intent = ""
    gamemode = False
    device_owner = None
    device = None
    session_data = {}
    item = ""
    position = ""
    preposition = ""
    original_sentence = ""

    def __init__(self, req={}):

        self.response = ResponseDUEROS()
        self.response.setPlantText(HELP_MSG)
        self.request = req
        self.request_type = req["request"]["type"]
        if self.request_type == "IntentRequest":
            self.intent = req["request"]["intents"][0]["name"]
            '''
            读取slot数据，item为演示数据
            '''

            if "slots" in req["request"]["intents"][0]:
                if "item" in req["request"]["intents"][0]["slots"]:
                    self.item = req["request"]["intents"][0]["slots"]["item"]["value"]

        uid = req["context"]["System"]["user"]["userId"]

        (self.device_owner, created) = BOT_DeviceOwner.objects.get_or_create(userid=uid)
        (self.device, created) = BOT_Device.objects.get_or_create(
            deviceid=req["context"]["System"]["device"]["deviceId"],
            ownerid=self.device_owner)

        '''
        读取通过session数据传递的上次数据，gamemode为演示数据

        '''
        if "attributes" in req["session"]:
            if "gamemode" in req["session"]["attributes"]:
                self.gamemode = req["session"]["attributes"]["gamemode"]

        '''
        读取原始语句
        '''
        if "query" in req["request"]:
            if "original" in req["request"]["query"]:
                self.original_sentence = req["request"]["query"]["original"]

        return

    def launchRequest(self):

        self.response.setPlantText(START_MSG)
        self.gamemode = False
        return self.response

    def intent_process(self):
        item = ""
        '''
        系统意图处理，全部系统意图见
            https://dueros.baidu.com/didp/doc/dueros-bot-platform/dbp-nlu/system_intents_markdown
        '''
        if self.intent == "ai.dueros.common.default_intent":
            self.response.add_session_data(False, "gamemode")
            self.response.setPlantText(AGAIN_MSG)
        elif self.intent == "ai.dueros.common.cancel_intent)":
            self.response.shouldEndSession = True
            self.response.setPlantText(EXIT_MSG)
            '''
                自定义意图处理

            '''
        elif self.intent == "gamemode":
            self.response.add_session_data(True, "gamemode")
            self.response.setPlantText(GAME_STAET_MSG)

        return self.response
