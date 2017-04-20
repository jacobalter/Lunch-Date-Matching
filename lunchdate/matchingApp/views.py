from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader
import django_tables2 as tables
from .models import Person
from .models import Restaurant
from django.shortcuts import render

def index(request):
    return render_to_response('index.html')


def queryOut(request, person_id):
    template = loader.get_template('queryOut.html')
    sp = Person.objects.get(pk=person_id)
    restaurant = Restaurant.objects.all()
    people = Person.objects.all()
    context = {
        'sp':sp,
        'restaurant': Restaurant.objects.all(),
        'people': Person.objects.all(),
        
    }

    return HttpResponse(template.render(context, request), sp)
        
def matchUser(request, person_id):
    template = loader.get_template('matchUser.html')
    sp = Person.objects.get(pk=person_id)
    restaurant = Restaurant.objects.all()
    people = Person.objects.all()
    context = {
        'sp':sp,
        'restaurant': Restaurant.objects.all(),
        'people': Person.objects.all(),
        
    }

    return HttpResponse(template.render(context, request), sp)

def matchUserNow(request, person_id):
    template = loader.get_template('matchUserNow.html')
    sp = Person.objects.get(pk=person_id)
    restaurant = Restaurant.objects.all()
    people = Person.objects.all()
    context = {
        'sp':sp,
        'restaurant': Restaurant.objects.all(),
        'people': Person.objects.all(),
        
    }

    return HttpResponse(template.render(context, request), sp)

def addFriends(request, person_id):
    template = loader.get_template('addFriends.html')
    sp = Person.objects.get(pk=person_id)
    restaurant = Restaurant.objects.all()
    people = Person.objects.all()
    context = {
        'sp':sp,
        'restaurant': Restaurant.objects.all(),
        'people': Person.objects.all(),
        
    }

    return HttpResponse(template.render(context, request), sp)

def settings(request, person_id):
    template = loader.get_template('settings.html')
    sp = Person.objects.get(pk=person_id)
    restaurant = Restaurant.objects.all()
    people = Person.objects.all()
    context = {
        'sp':sp,
        'restaurant': Restaurant.objects.all(),
        'people': Person.objects.all(),
        
    }
    return HttpResponse(template.render(context, request), sp)

def findRestaurant(request, person_id):
    template = loader.get_template('findRestaurant.html')
    sp = Person.objects.get(pk=person_id)
    restaurant = Restaurant.objects.all()
    people = Person.objects.all()
    context = {
        'sp':sp,
        'restaurant': Restaurant.objects.all(),
        'people': Person.objects.all(),
        
    }

    return HttpResponse(template.render(context, request), sp)

    


def registerUser(request):
    
    template = loader.get_template('queryOut.html')
    sp = Person.objects.get(pk=person_id)
    restaurant = Restaurant.objects.all()
    people = Person.objects.all()
    context = {
        'sp':sp,
        'restaurant': Restaurant.objects.all(),
        'people': Person.objects.all(),
        
    }
    return HttpResponse(template.render(context, request), sp)