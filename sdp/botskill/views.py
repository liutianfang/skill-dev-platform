from django.http import HttpResponse
from django.http import JsonResponse
from botskill.models import BOT_Log
import json, time
from django.views.decorators.csrf import csrf_exempt
from botskill.processer import *



EXCEPT_MSG = "系统有点故障，等一下再试试吧"
EXIT_MSG = "再见，我会一直等着你哦"


@csrf_exempt
def index(request):
    start = time.time()
    exmsg = ""
    response = ResponseDUEROS()
    request_type = ""
    requestVar = {}
    dblog = BOT_Log()

    if request.method == 'POST':
        try:
            # logger.info("POST process start ")
            requestVar = json.loads(request.body, encoding='utf-8')
            dblog.request = json.dumps(requestVar, ensure_ascii=False)
            dblog.ip = get_ip(request)
            dblog.header = meta(request)
            dblog.save()
            request_type = requestVar["request"]["type"]
        except  Exception as e :
            response.shouldEndSession = True
            response.response["output"] = {"type": "PlainText", "text": EXCEPT_MSG}
            dblog.exmsg = "Exception:" + str(e)
            dblog.save()
            return JsonResponse(response.to_dict(), safe=False, )
    else:  # GET

        return HttpResponse("service is working")

    # response.contexts["last_request_type"] = request_type
    if (request_type == "SessionEndedRequest"):
        response.set_session_end()
        response.response["output"] = {"type": "PlainText", "text": EXIT_MSG}
        return JsonResponse(response.to_dict(), safe=False)

    processer = Processer(requestVar)

    if (request_type == "LaunchRequest"):
        processer.launchRequest();
    elif (request_type == "IntentRequest"):
         processer.intent_process()

    response=processer.response
    dblog.response = json.dumps(response.to_dict(), ensure_ascii=False)
    end = time.time()
    dblog.exmsg = str(exmsg) + "\r\n process time=" + "{:.3f}".format((end - start))
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
        if k.startswith("HTTP") or k.startswith("CONTENT_"):
            info += '{} : {}\r\n'.format(k, v)
    return info
