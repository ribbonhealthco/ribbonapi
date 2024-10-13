
from django.http import JsonResponse

def index(request):
    data = {
        "message": "Ribbon Health API",
        "status": "success"
    }
    return JsonResponse(data)
