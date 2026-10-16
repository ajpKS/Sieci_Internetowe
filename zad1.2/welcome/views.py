from datetime import datetime, date
from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Welcome to Django!")
# Create your views here.
def hello_name(request, name):
    return HttpResponse(f"Hello {name}")

def hello_template(request, name):
    return render(request, "welcome/hello.html", {"name": name})

def time(request):

    return HttpResponse(f"Today's date is: {date.today()}, and time is {datetime.now().hour}:{datetime.now().minute}")
