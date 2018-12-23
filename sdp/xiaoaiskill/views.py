from django.http import HttpResponse
from django.http import JsonResponse
import json,time
from django.views.decorators.csrf import csrf_exempt
from xiaoaiskill.processer import Processer
from xiaoaiskill.MiResponse import MiResponse
from xiaoaiskill.models import *


WAKEUP_WORD="小爱同学"
# doc https://xiaoai.mi.com/documents/Home?type=/api/doc/render_markdown/SkillAccess/SkillDocument/CustomSkills/CustomSkillsMain

EXIT_MSG="好的，再见，我会一直等着你哦"

EXCCPT_MSG="我有点小问题，换个说法吧"
UNKNOWN_MSG = "抱歉，我没听懂，请再说一次吧"
WELCOME_MSG = "欢迎您的到来"



@csrf_exempt
def index(request):
    start = time.time()
    exmsg=""
    response=MiResponse()
    request_type=0
    req_dict={}
    dblog=MI_Log()
    processer=None

    if request.method == 'POST':
        try:
            # logger.info("POST process start ")
            req_dict = json.loads(request.body,encoding='utf-8')
            # 心跳检测
            if req_dict["request"]["type"] == 0:
                if  "slot_info" in req_dict["request"]:
                    if  "intent_name" in req_dict["request"]["slot_info"]:
                        if req_dict["request"]["slot_info"]["intent_name"]=="Mi_Welcome" and req_dict["request"]["is_monitor"]==True :
                            response.tts_text_out("welcome")
                            return JsonResponse(response.to_dict(), safe=False, )

            dblog.request=json.dumps(req_dict,ensure_ascii= False)
            dblog.ip=get_ip(request)
            dblog.header=meta(request)
            dblog.save()
            request_type = req_dict["request"]["type"]
        except  Exception:
            response.shouldEndSession = True
            response.tts_text_out(EXCCPT_MSG)
            dblog.exmsg="Exception:"+str(Exception)
            dblog.save()
            response.tts_text_out(EXCCPT_MSG)
            return JsonResponse(response.to_dict(), safe=False, )
    else: #GET

        return HttpResponse("service is working")

    if (request_type == 0 ):
        response.tts_text_out(WELCOME_MSG)
    # 退出
    elif (request_type == 2):
        response.end_session()
        response.tts_text_out(EXIT_MSG)
    elif (request_type == 1):
        # try:
            processer = Processer(req_dict)
            processer.intent_process()
            response = processer.response
        # except Exception:
        #
        #     print("ExceptionS")
        #     response.tts_text_out(EXCCPT_MSG)
        #     exmsg=str(Exception)
    else:
        response.tts_text_out(UNKNOWN_MSG)

    dblog.response=json.dumps(response.to_dict(), ensure_ascii= False)
    dblog.deviceid=processer.device
    dblog.ownerid=processer.device_owner

    end = time.time()
    dblog.exmsg= json.dumps({"Exception":exmsg,"process time":"{:.3f}".format((end - start))})
    dblog.save()

    return JsonResponse(response.to_dict(), safe=False)

# 获取请求IP
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

'''
获取请求头信息
'''
def meta(request):
    META = request.META
    info = ''
    for k, v in META.items():
        if k.startswith("HTTP") or k.startswith("CONTENT_") or  k.startswith("REMOTE") or k.startswith("SERVER") or k.startswith("REQUEST") :
            info += '\r\n{} : {}\r\n'.format(k, v)
    return info
