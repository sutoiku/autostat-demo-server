from django.shortcuts import render
from django.http import HttpResponse

# from .models import Greeting/
import json

# Create your views here.
def index(request):
    data = json.loads("[" + request.GET.get("data", "") + "]")
    return HttpResponse(f"Hello from Python!\n{str([x**3 for x in data])}\n\n")
    # return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
