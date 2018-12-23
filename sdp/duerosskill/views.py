from django.http import HttpResponse
from django.http import JsonResponse
import json, time
from django.views.decorators.csrf import csrf_exempt
# import logging
from duerosskill.processer import *
from duerosskill.models import *
from duerosskill.response import ResponseDUEROS


EXCEPT_MSG = "系统有点故障，等一下再试试吧"
EXIT_MSG = "再见，我会一直等着你哦"


@csrf_exempt
def index(request):
    start = time.time()
    exmsg = ""
    # logger = logging.getLogger('django')
    response = ResponseDUEROS()
    request_type = ""
    requestVar = {}
    processer=None
    dblog = Dueros_Log()
    userid=0
    intent=''
    if request.method == 'POST':
        try:
            # logger.info("POST process start ")
            requestVar = json.loads(request.body, encoding='utf-8')
            dblog.json_request = json.dumps(requestVar, indent=1, ensure_ascii=False)
            print(dblog.json_request)
            dblog.bin_request=request.body
            dblog.ip = get_ip(request)
            dblog.header = meta(request)
            dblog.save()
            request_type = requestVar["request"]["type"]
        except  Exception:
            # logger.info("POST  except= " + str(Exception))

            response.shouldEndSession = True
            response.tts_output(EXCEPT_MSG)
            dblog.exmsg = "Exception:" + str(repr(Exception))
            dblog.save()
            return JsonResponse(response.to_dict(), safe=False, )
    else:  # GET

        return HttpResponse("service is working")

    if (request_type == "SessionEndedRequest"):
        response.set_session_end()
        response.tts_output(EXIT_MSG)
    else:

        processer = Processer(requestVar)
        userid=processer.device_owner.id
        if (request_type == "LaunchRequest"):
            processer.launchRequest()
        elif (request_type == "IntentRequest"):
            processer.intent_process()
            intent=processer.intent
        response = processer.response

    dblog.useid=userid
    dblog.intent=intent
    dblog.response = json.dumps(response.to_dict(), ensure_ascii=False)
    dblog.deviceid=processer.device
    dblog.ownerid=processer.device_owner
    end = time.time()
    dblog.exmsg = str(exmsg) + " process time=" + "{:.3f}".format((end - start))+"\r\n"+"intent="+intent
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
        if k.startswith("HTTP") or k.startswith("CONTENT_") or  k.startswith("REMOTE") or k.startswith("SERVER") or k.startswith("REQUEST_URI") :
            info += '{} : {}\r\n'.format(k, v)
    return info
