from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, from Educative Django Blog App!")
