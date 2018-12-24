from jdskill.models import *
import random, datetime
from typing import *
from jdskill.response import ResponseJD

MY_NAME = "我的应用"
START_MSG = "你好，我是" + MY_NAME+"，欢迎使用"

HELP_MSG = "帮助信息"
AGAIN_MSG = "我没有听明白，再说一次吧"
EXIT_MSG = "再见"
GAME_STAET_MSG = "游戏开始"


class Processer(object):
    request = {}
    response = None
    request_type = ""
    intent = ""
    gamemode = False
    device_owner = None
    device = None
    session_data = {}
    original_sentence = ""
    slot_values = {}

    def __init__(self, req: Dict):

        self.response = ResponseJD()
        self.response.set_output_plantText(HELP_MSG)
        self.request = req

        self.request_type = req["request"]["type"]
        if self.request_type == "IntentRequest":
            self.intent = req["request"]["intents"]["name"]
            '''
            读取slot数据，item为演示数据
            '''

            if "slots" in req["request"]["intents"][0]:
                if "item" in req["request"]["intents"][0]["slots"]:
                    self.item = req["request"]["intents"][0]["slots"]["item"]["value"]

        uid = req["session"]["user"]["userId"]

        (self.device_owner, created) = JD_DeviceOwner.objects.get_or_create(userid=uid)
        (self.device, created) = JD_Device.objects.get_or_create(deviceid=req["session"]["device"]["deviceId"],
                                                                 ownerid=self.device_owner)

        self.slot_values = {}

        if "intent" in req["request"]:
            if "slots" in req["request"]["intent"]:
                for key in req["request"]["intent"]["slots"]:
                    self.slot_values = req["request"]["intent"]["slots"][key]["value"]

        # 读取session数据

        if "contexts" in self.request["session"]:
            self.session_data = self.request["session"]["contexts"]

        # 读取原始语句
        if "original" in req:
            self.original_sentence = req["original"]

        return

    def launchRequest(self):

        self.response.set_output_plantText(START_MSG)
        self.gamemode = False
        return
    def intent_process(self):

        return
