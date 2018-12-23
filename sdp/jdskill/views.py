from django.http import HttpResponse
from django.http import JsonResponse
import json, time
from django.views.decorators.csrf import csrf_exempt
import logging
from jdskill.response import ResponseJD
from jdskill.models import *
from jdskill.processer import Processer
from typing import *


START_MSG= "启动信息"

HELP_MSG= "帮助信息"
EXIT_MSG="好的，再见，我会一直等着你哦"


@csrf_exempt
def index(request):
    start = time.time()
    # exmsg={}
    # logger = logging.getLogger('django')
    response=ResponseJD()
    request_type=""
    request_dict={}
    dblog=JD_Log()
    exception=''

    if request.method == 'POST':
        try:
            request_dict = json.loads(request.body,encoding='utf-8')
            dblog.request = json.dumps(request_dict, ensure_ascii=False)
            dblog.ip=get_ip(request)
            dblog.header=meta(request)
            request_type = request_dict["request"]["type"]
        except  Exception:
            dblog.exmsg=str(Exception )
            response.shouldEndSession = True
            response.set_output_plantText(EXIT_MSG)
            return JsonResponse(response.to_dict(), safe=False, )
    else: #GET

        return HttpResponse("service is working")

    response.add_session_data( request_type,"last_request_type")
    if (request_type == "SessionEndedRequest"):
        response.set_session_end()
        response.set_output_plantText(EXIT_MSG)
        return JsonResponse(response.to_dict(), safe=False)

    processer = Processer(request_dict)

    if (request_type == "LaunchRequest"):
        processer.launchRequest()
    elif (request_type == "IntentRequest"):
        processer.intent_process()

    response = processer.response
    dblog.response = json.dumps(response.to_dict(), ensure_ascii=False)
    dblog.deviceid=processer.device
    dblog.ownerid=processer.device_owner
    end = time.time()
    dblog.exmsg = " {\"process time\":" + "{:.3f}".format((end - start))
    dblog.save()

    return JsonResponse(response.to_dict(), safe=False)



def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def meta(request):
    META = request.META
    info = ''
    for k, v in META.items():
        if k.startswith("HTTP") or k.startswith("CONTENT_") or  k.startswith("REMOTE") or k.startswith("SERVER") or k.startswith("REQUEST_URI") :
            info += '\r\n{} : {}\r\n'.format(k, v)
    return info
