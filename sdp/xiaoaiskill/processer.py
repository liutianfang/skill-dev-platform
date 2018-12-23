from xiaoaiskill.models import *
from xiaoaiskill.MiResponse import MiResponse
import random, datetime

WAKEUP_WORD = "小爱同学"
MY_NAME = "我的应用"
START_MSG = "你好，我是" + MY_NAME + "需要使用帮助请和我说：帮助"

EXIT_MSG = "再见，我会一直等着你再来哦"

NO_UNDERSTAND = "抱歉，我没听懂，请再说一次吧"

HELP_WORDS = {"帮助", "怎么用", "怎么玩", }

SKIP_WORDS = {"跳过"}
QUIT_WORDS = {"退出", "退出" + MY_NAME, "离开", "离开" + MY_NAME, "关闭", "关闭" + MY_NAME}
DENY_WORDS = {"不是", "不对", "忘了吧", "错了", "错误"}

PROMPT_MSG = "嗯哼"
HELP_MSG = "嗯哼"
WELCOME_MSG = "欢迎"


class Processer(object):
    request = None
    response = None
    request_type = 0
    intent = ""
    device_owner = None
    device = None
    session_data = None
    slots_vaule = None
    original_sentence = ""

    def __init__(self, req):

        self.original_sentence = ""
        self.session_data = {}
        self.slots_vaule = {}
        self.response = MiResponse()

        self.request = req
        self.request_type = req["request"]["type"]
        self.original_sentence = req["query"].strip()
        #  get session data
        if "attributes" in self.request["session"]:
            self.session_data = self.request["session"]["attributes"]

        if self.request_type == 1:
            if "slot_info" in req["request"]:
                if "intent_name" in req["request"]["slot_info"]:
                    self.intent = req["request"]["slot_info"]["intent_name"]

        uid = req["session"]["user"]["user_id"]
        (self.device_owner, created) = MI_DeviceOwner.objects.get_or_create(userid=uid)
        if "device_id" in req["context"]:
            (self.device, created) = MI_Device.objects.get_or_create(deviceid=req["context"]["device_id"],
                                                                     ownerid=self.device_owner)

        # get slots vaule
        if "slot_info" in req["request"]:
            if "slots" in req["request"]["slot_info"]:
                slots = req["request"]["slot_info"]["slots"]
                for slot in slots:
                    self.slots_vaule[slot["name"]] = slot["value"]

        return

    def launchRequest(self):

        self.response.tts_text_out(WELCOME_MSG)
        return self.response

    def intent_process(self):
        intent = self.intent

        if intent == "Mi_Welcome":
            self.launchRequest()
            return self.response
        elif intent == "Mi_Exit":
            self.response.tts_text_out(EXIT_MSG)
            self.response.end_session()
            return self.response
        # xiaoai专有处理
        elif self.original_sentence in SKIP_WORDS:
            self.intent = "skip"
            self.response.tts_text_out("嗯")
            return self.response

        #  用户无反应请求，返回提醒信息
        if "no_response" in self.request["request"]:
            if self.request["request"]["no_response"] == True and self.original_sentence == "":
                if "nrc" in self.session_data:  # nrc no_response_counter
                    if self.session_data["nrc"] > 3:
                        #  退出
                        self.response.tts_text_out(EXIT_MSG)
                        self.response.set_session_value(0, "nrc")
                        self.response.end_session()
                    else:
                        if "prompt" in self.session_data:
                            self.response.tts_text_out(self.session_data['prompt'])
                        else:
                            self.response.tts_text_out(PROMPT_MSG)
                        self.response.set_session_value(self.session_data["nrc"] + 1, "nrc")
                else:
                    msg = PROMPT_MSG
                    self.response.set_session_value(1, "nrc")

                for key in self.session_data:
                    self.response.set_session_value(self.session_data[key], key)
                self.response.set_session_value(1, "go")
                return self.response

        #  add  your rpocess here,follow codes are demo  process

        for key in self.session_data:
            self.response.set_session_value(self.session_data[key],key)

        self.response.tts_text_out(WELCOME_MSG)


        return self.response
