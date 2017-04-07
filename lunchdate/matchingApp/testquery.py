from django.db import models
from matchingApp.models import Restaurant


from matchingApp.models import 

a = Restaurant.objects.filter(name__contains='').values()

print(a)

from matchingApp.models import Person

sp = Person.objects.filter(id = '19').values()
pc = Person.objects.count()

print(pc)
print(sp)