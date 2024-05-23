from django_apis.views import get_apiview
from django_apis.views import get_json_payload
from django_apis.exceptions import InputValidationError
from .forms import EchoInput

apiview = get_apiview()


@apiview(methods="GET")
def ping(request):
    return "pong"


@apiview(methods="POST")
def echo(request):
    payload = get_json_payload(request)
    form = EchoInput(payload)
    if not form.is_valid():
        raise InputValidationError(form)
    return form.cleaned_data["msg"]


@apiview(methods="GET")
def getRequestInfo(request):
    result = {}
    for key, value in request.META.items():
        if isinstance(value, str):
            result[key] = value
    return result
