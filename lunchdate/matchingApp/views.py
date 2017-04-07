from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader
import datetime
from .models import Person

def index(request):
    return render_to_response('index.html')

def login(request):
	return HttpResponse("Login Page")

def queryOut(request, person_id):

    sp = Person.objects.filter(id = person_id).values()
    
    return HttpResponse(sp)
	