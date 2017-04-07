from django.http import HttpResponse
import datetime
from .models import Person

def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def login(request):
	return HttpResponse("Login Page")

def queryOut(request, person_id):

    sp = Person.objects.filter(id = person_id).values()
    
    return HttpResponse(sp)
	