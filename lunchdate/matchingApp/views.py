from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
import django_tables2 as tables
from .models import *
from django.shortcuts import render
import datetime
from math import *
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from math import *
from django.db import connection, transaction

	
def index(request):
    return render_to_response('index.html')
	
def get_location(person, time, day):
    person_location = list(BusyAt.objects.raw('''SELECT * FROM busy_at WHERE userid = %s order by weekday, timeblock''', [person.id]))
    for i in range(0, len((person_location))):
        if int(person_location[i].weekday) < 1:
            pass
        elif int(person_location[i].weekday) == day:
            while(int(person_location[i].weekday) == day and i < len(person_location) and ((person_location[i].timeblock.hour * 100) + person_location[i].timeblock.minute + 30) < time):
                i += 1
            i -= 1
            
            break
        else:
            i -= 1
            break
    return person_location[i]
   
def distance_sorter(self, cur_location, time, day):
    person_location = get_location(self, time, day)
    distance = vincenty((person_location.latitude, person_location.longitude), (cur_location.latitude, cur_location.longitude)).miles
    return distance
	
def restaurant_sorter(self, possible_restaurants, cur_location, fr_location):
    your_prefs = len(possible_restaurants[self][0])
    fr_prefs = len(possible_restaurants[self][1])
    both_prefs = len(possible_restaurants[self][2])
    score = 0
    score += (both_prefs * 2) + (fr_prefs) + (your_prefs)
    their_distance = vincenty((self.latitude, self.longitude), (fr_location.latitude, fr_location.longitude)).miles
    score -= their_distance
    score += 1
    return "%.2f" % (score)
    
    

def queryOut(request, person_id):
    template = loader.get_template('queryOut.html')
    if not Person.objects.filter(id = person_id).exists():
        return HttpResponseRedirect("/")
    sp = Person.objects.get(pk=person_id)
    people = Person.objects.all()
    
    hours = []
    hours.append("-")
    for i in range (0, 24):
        hours.append(i)
    minutes = ["-", 0, 30]
    days = ["-", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    possible_friends = Friends.objects.filter(user1 = person_id) | Friends.objects.filter(user2 = person_id)
    temp_friends = []
    for friend in possible_friends:
        if int(friend.user1.id) == int(person_id):
            temp_friends.append(friend.user2)
        else:
            temp_friends.append(friend.user1)
    context = {
        'sp':sp,
		'hours': hours,
		'minutes' : minutes,
		'daysL' : days,
		'friends' : temp_friends,
        
    }

    return HttpResponse(template.render(context, request), sp)
	
def getMatchRestaurant(request, fr_id, person_id, day, time, dist):
    template = loader.get_template('matchRestaurant.html')
    sp = Person.objects.get(pk=person_id)
    fr = Person.objects.get(pk=fr_id)
    day = int(day)
    if(day == 0):
        daystr = "Monday"
    elif(day == 1):
        daystr = "Tuesday"
    elif(day == 2):
        daystr = "Wednesday"
    elif(day == 3):
        daystr = "Thursday"
    elif(day == 4):
        daystr = "Friday"
    elif(day == 5):
        daystr = "Saturday"
    else:
        daystr = "Sunday"
    truetime = time[:-2] + ":" + time[-2:]
    minute = int(truetime[-2])
    if(minute >= 3):
        minute = 30
    else:
        minute = 0
    if len(time) > 2:
        hour = int(time[:-2])
    else:
        hour = 0
        truetime = "0" + ":" + time[-2:]
    time = (hour * 100) + minute
	
    all_restaurants = Restaurant.objects.filter()
    valid = []
    cur_location = get_location(sp, time, int(day))
    for r in all_restaurants:
        distance = vincenty((r.latitude, r.longitude), (cur_location.latitude, cur_location.longitude)).miles
        times = OpenAt.objects.filter(restaurantid = r.restaurantid, weekday = int(day))
        found_open = 0
        for t in times:
            open = t.open_time
            close = t.close_time
            if(close < open):
                close = 2400
            if open <= time and time <= close:
                found_open = 1
                break	
		#check open day before
        times = OpenAt.objects.filter(restaurantid = r.restaurantid, weekday = (int(day) - 1) % 7)
        for t in times:
            open = t.open_time
            close = t.close_time
            if(close < open):
                if(0 <= time and time <= close):
                    found_open = 1
                    break
        if distance <= int(dist) and found_open == 1:
			#dining halls
            if not ((r.restaurantid == 201 or r.restaurantid == 202) and (sp.has_meal_plan == False or fr.has_meal_plan == False)):
                valid.append(r.restaurantid)
    possible_restaurants = Restaurant.objects.filter(restaurantid__in = valid)
	
    your_preferences = Likes.objects.filter(userid = person_id)
    your_prefs = []
    for p in your_preferences:
        your_prefs.append(p.food_type)
		
	
    f_preferences = Likes.objects.filter(userid = fr.id)
    f_prefs = []
    for i in f_preferences:
        f_prefs.append(i.food_type)
		
		
    match_dict = {}
    for r in possible_restaurants:
        sells = SoldBy.objects.filter(restaurantid = r.restaurantid)
        sells_list = []
        for s in sells:
            sells_list.append(s.food_type)
			
        overlap = list(set(your_prefs) & set(sells_list))
        match_dict[r] = [overlap]
        overlap = list(set(f_prefs) & set(sells_list))
        match_dict[r].append(overlap)
        overlap = list(set(f_prefs) & set(your_prefs) & set(sells_list))
        match_dict[r].append(overlap)

    restaurants_list = []
    fr_location = get_location(fr, time, int(day))
    for r in possible_restaurants:
        temp_score = (r.name, float(restaurant_sorter(r, match_dict, cur_location, fr_location)))
        restaurants_list.append(temp_score)
    restaurants_list = sorted(restaurants_list, key=lambda x: x[1], reverse = True)
    restaurants_list = restaurants_list[:10]
	
	
    context = {
        'sp':sp,
		'fr' : fr,
        'restaurants' : restaurants_list,
		'overlap' : match_dict,
		'day' : daystr,
		'truetime' : truetime,
    }

    return HttpResponse(template.render(context, request), sp)

def matchUserNow(request, person_id, distance, hour, minute, day):
    template = loader.get_template('matchUserNow.html')
    sp = Person.objects.get(pk=person_id)
    maxdist = distance

    time = datetime.datetime.now()
    if(hour == "-"):
        hour = time.hour
    else:
        hour = int(hour)
    if(minute == "-"):
        minute = time.minute
    else:
        minute = int(minute)

    days = {"-": "-", "Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
    day = days[day]
    if(day == "-"):
        day = datetime.date.today().weekday()
    truetime = (hour * 100) + minute
    if(minute > 30):
        minute = 30
        time_str = str(hour) + ":" + str(30)
    else:
        minute = 0
        time_str = str(hour) + ":" + "00"
    time = (hour * 100) + minute
	
    #find person's location
    cur_location = get_location(sp, time, day)
	#if allows strangers
    if sp.allow_strangers == True:
        temp_friends = list(Person.objects.filter(allow_strangers = True).exclude(id = person_id))
    #if does not allow strangers
    else:
		#all friends
        possible_friends = Friends.objects.filter(user1 = person_id) | Friends.objects.filter(user2 = person_id)
        temp_friends = []
        for friend in possible_friends:
            if int(friend.user1.id) == int(person_id):
                temp_friends.append(friend.user2)
            else:
                temp_friends.append(friend.user1)
				
    to_be_deleted = []
    #delete friends who are busy
    for person in temp_friends:
        person_busy_times = BusyAt.objects.filter(userid = person.id)
        if person_busy_times.filter(timeblock = time_str, weekday = str(day)).exists():
            to_be_deleted.append(person.id)
				
    for id in to_be_deleted:
        for friend in temp_friends:
            if friend.id == id:
                temp_friends.remove(friend)
				
    possible_friends_ids = []
    for friend in temp_friends:
        possible_friends_ids.append(friend.id)
    free_friends = list(Person.objects.filter(id__in = possible_friends_ids))

    #all friends who are not busy
    possible_friends = sorted(free_friends, key = lambda elem: distance_sorter(elem, cur_location, time, day))
    possible_friends = possible_friends[:10]
    distances = []
    for fr in possible_friends:
        f = get_location(fr, time, day)
        distance = vincenty((f.latitude, f.longitude), (cur_location.latitude, cur_location.longitude)).miles
        distances.append(distance)

    your_preferences = Likes.objects.filter(userid = person_id)
    your_prefs = []
    for p in your_preferences:
        your_prefs.append(p.food_type)
	
	#all friends
    your_p_friends = Friends.objects.filter(user1 = person_id) | Friends.objects.filter(user2 = person_id)
    your_friends = []
    for friend in your_p_friends:
        if int(friend.user1.id) == int(person_id):
            your_friends.append(friend.user2)
        else:
            your_friends.append(friend.user1)
		
	#get preference intersection
    in_common_list = []
    f_in_common_list = []
    for fr in possible_friends:
        f_prefs = []
        f_preferences = Likes.objects.filter(userid = fr.id)
        for f in f_preferences:
            f_prefs.append(f.food_type)
        in_common = list(set(f_prefs) & set(your_prefs))
        in_common_list.append(in_common)
	
        p_friends = Friends.objects.filter(user1 = fr.id) | Friends.objects.filter(user2 = fr.id)
        fr_friends = []
        for friend in p_friends:
            if int(friend.user1.id) == int(fr.id):
                fr_friends.append(friend.user2)
            else:
                fr_friends.append(friend.user1)
		
        in_common = list(set(fr_friends) & set(your_friends))
        f_in_common_list.append(in_common)
		
    table_list = []
    for i in range (0,len(possible_friends)):
        temp = []
        temp.append(possible_friends[i])
        dist = ceil(distances[i]*100)/100
        temp.append(dist)
        temp_str = "" 
        if(len(in_common_list[i]) > 0):
            temp_str += in_common_list[i][0]
        for j in in_common_list[i][1:]:
            temp_str += ", "
            temp_str += j
        temp.append(temp_str)
		
        temp_str = "" 
        if(len(f_in_common_list[i]) > 0):
            temp_str += f_in_common_list[i][0].name
        for j in f_in_common_list[i][1:]:
            temp_str += ", "
            temp_str += j.name
        temp.append(temp_str)
        table_list.append(temp)
            
    context = {
        'sp':sp,
		'table' : table_list,
		'day' : day,
		'time' : truetime,
		'distance' : maxdist
    }
	
    return HttpResponse(template.render(context, request), sp)

def addFriends(request, person_id):
    template = loader.get_template('addFriends.html')
    sp = Person.objects.get(pk=person_id)
    context = {
        'sp':sp,
    }

    return HttpResponse(template.render(context, request), sp)
	
def friendEntry(request, person_id, fr_id):
    sp = Person.objects.get(pk=person_id)
    fr = Person.objects.get(pk=fr_id)
	
    cursor = connection.cursor()
    cursor.execute("select nextval('friends_id_seq')")
    result = cursor.fetchone()
	
    if sp.id > fr.id:
        if Friends.objects.filter(user1 = fr, user2 = sp).exists():
            pass
        else:
            newFriend = Friends(id = result[0], user1 = fr, user2 = sp)
            newFriend.save()
    elif fr.id > sp.id:
        if Friends.objects.filter(user1 = sp, user2 = fr).exists():
            pass
        else:
            newFriend = Friends(id = result[0], user1 = sp, user2 = fr)
            newFriend.save()
    else:
        pass

    return HttpResponseRedirect("/%d/" % sp.id)
	

def settings(request, person_id):
    template = loader.get_template('settings.html')
    sp = Person.objects.get(pk=person_id)
    context = {
        'sp':sp,
        
    }
    return HttpResponse(template.render(context, request), sp)

def findRestaurant(request, person_id):
    template = loader.get_template('findRestaurant.html')
    sp = Person.objects.get(pk=person_id)
    types = SoldBy.objects.all().distinct('food_type')
    hours = []
    hours.append("-")
    for i in range (0, 24):
        hours.append(i)
    minutes = ["-", 0, 30]
    days = ["-", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    context = {
        'sp':sp,
        'types': types,
		'hours' : hours,
		'minutes': minutes,
		'daysL' : days
    }

    return HttpResponse(template.render(context, request), sp)
	
def queryRestaurant(request, person_id, foodtype, dist, hour, minute, day):
    template = loader.get_template('queryRestaurant.html')
    sp = Person.objects.get(pk=person_id)

    trueminute = "-1"
    time = datetime.datetime.now()
    if(hour == "-"):
        hour = time.hour
    else:
        hour = int(hour)
    if(minute == "-"):
        minute = time.minute
        trueminute = str(datetime.datetime.now().minute)
    else:
        minute = int(minute)

    days = {"-": "-", "Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
    day = days[day]
    if(day == "-"):
        day = int(datetime.date.today().weekday())
    truetime = (hour * 100) + minute
    if(minute >= 30):
        minute = 30
        if(trueminute == "-1"):
            trueminute = "30"
    else:
        minute = 0
        if(trueminute == "-1"):
            trueminute = "30"
    time = (hour * 100) + minute
    time_str = str(hour) + ":" + trueminute
	
    if(day == 0):
        daystr = "Monday"
    elif(day == 1):
        daystr = "Tuesday"
    elif(day == 2):
        daystr = "Wednesday"
    elif(day == 3):
        daystr = "Thursday"
    elif(day == 4):
        daystr = "Friday"
    elif(day == 5):
        daystr = "Saturday"
    else:
        daystr = "Sunday"
	
    #find person's location
    cur_location = get_location(sp, time, day)
    all_restaurants = Restaurant.objects.all()
    valid = []
    for r in all_restaurants:
        distance = vincenty((r.latitude, r.longitude), (cur_location.latitude, cur_location.longitude)).miles
        times = OpenAt.objects.filter(restaurantid = r.restaurantid, weekday = int(day))
        found_open = 0
        for t in times:
            open = t.open_time
            close = t.close_time
            if(close < open):
                close = 2400
            if open <= time and time <= close:
                found_open = 1
                break	
		#check open day before
        times = OpenAt.objects.filter(restaurantid = r.restaurantid, weekday = (int(day) - 1) % 7)
        for t in times:
            open = t.open_time
            close = t.close_time
            if(close < open):
                if(0 <= time and time <= close):
                    found_open = 1
                    break
        if distance <= int(dist) and found_open == 1:
			#dining halls
            if not ((r.restaurantid == 201 or r.restaurantid == 202) and (sp.has_meal_plan == False)):
                sells = SoldBy.objects.filter(restaurantid = r.restaurantid)
                sells_list = []
                for s in sells:
                    sells_list.append(s.food_type)
                if foodtype in sells_list:
                    valid.append(r.restaurantid)
    possible_restaurants = Restaurant.objects.filter(restaurantid__in = valid)
	
    context = {
        'sp':sp,
        'time' : time_str,
        'day' : daystr,
		'type' : foodtype,
		'restaurants' : possible_restaurants,
		'dist' : dist
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

def updateUser(request, person_id, newname, mealplan, strangers):
    sp = Person.objects.get(pk=person_id)
	
    if(newname != ""):
        sp.name = newname
        sp.save() 
		
    if(mealplan == "T"):
        sp.has_meal_plan = True
        sp.save()	
    elif(mealplan == "F"):
        sp.has_meal_plan = False
        sp.save()
		
    if(strangers == "T"):
        sp.allow_strangers = True
        sp.save()	
    elif(strangers == "F"):
        sp.allow_strangers = False
        sp.save()		

    return HttpResponseRedirect("/%d/" % sp.id)

def addConflicts(request, person_id):
    template = loader.get_template('addConflicts.html')
    sp = Person.objects.get(pk=person_id)
    hours = []
    for i in range (0, 24):
        hours.append(i)
    minutes = [ 0, 30]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    allbuildings = Buildings.objects.all()
    buildings = []
    buildings.append("-")
    for b in allbuildings:
        buildings.append(b.name)
    context = {
        'sp':sp,
		'hours' : hours,
		'minutes': minutes,
		'buildings' : buildings
    }
    return HttpResponse(template.render(context, request), sp)
	
def updateConflict(request, person_id, hour, minute, day, address, building):
    sp = Person.objects.get(pk=person_id)
    geolocator = Nominatim()
    if address != "":
            location = geolocator.geocode(address) 
    else:
        location = Buildings.objects.get(name = building)
    if(location != None):
        latitude = location.latitude
        longitude = location.longitude
        time = str(hour) + ":" + str(minute)
        days = {"M": "0", "T": "1", "W": "2", "R": "3", "F": "4", "S": "5", "U": "6"}
        for d in day:
            cursor = connection.cursor()
            cursor.execute("select nextval('busy_at_id_seq')")
            result = cursor.fetchone()
            result = result[0]
            conflict = BusyAt(id = result, weekday = days[d], userid = sp, latitude = latitude, longitude = longitude, timeblock = time)
            conflict.save()
    return HttpResponseRedirect("/%d/" % sp.id)
	
def newUser(request, name, mealplan, strangers):

    cursor = connection.cursor()
    cursor.execute("select nextval('userseq')")
    result = cursor.fetchone()
    result = result[0]
    if strangers == "T":
        strangers = True
    else:
        strangers = False
    if mealplan == "T":
        mealplan = True
    else:
        mealplan = False
    newuser = Person(id = result, name = name, allow_strangers = strangers, has_meal_plan = mealplan)
    newuser.save()	
    return HttpResponseRedirect("/%d/" % result)



	
	
	
