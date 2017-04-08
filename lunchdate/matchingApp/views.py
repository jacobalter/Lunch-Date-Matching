from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader
import datetime
from .models import Person
from .models import Restaurant

def index(request):
    return render_to_response('index.html')


def queryOut(request, person_id):
    sp = Person.objects.get(pk=person_id)
    restaurant_output = Restaurant.objects.all().values()
    template = loader.get_template('queryOut.html')
    context = {
        'restaurant_output': restaurant_output,
        'sp':sp,
    }
    return HttpResponse(template.render(context, request), sp)
        
    