from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    context= {
        "message": "Heo Django Devs"
    }
    return render(request, "mysite/index.html", context)