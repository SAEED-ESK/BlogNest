from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from .tasks import sendEmail

import requests

def send_email(request):
    """
    A test task for testing celery
    """
    sendEmail.delay()
    return HttpResponse('<h1>Done sending</h1>')

@cache_page(60)
def test(request):
    """
    A test func for testing cashing
    """
    url = "https://ba646c97-a0ed-428f-a9d0-567c27a591c7.mock.pstmn.io/test/delay/5"
    response = requests.get(url)
    return JsonResponse(response.json())