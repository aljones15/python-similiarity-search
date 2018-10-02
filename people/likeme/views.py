from django.http import JsonResponse

# Create your views here.

def index(request):
    params = request.GET
    return JsonResponse({'peopleLikeYou': []})
