
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

class BusyAt(models.Model):
    weekday = models.CharField(max_length = 5)
    timeblock = models.TimeField()
    userid = models.ForeignKey('Person', models.DO_NOTHING, db_column='userid')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'busy_at'
        unique_together = (('userid', 'weekday', 'timeblock'),)

class Friends(models.Model):
    user1 = models.ForeignKey('Person', models.DO_NOTHING, related_name = "user1")
    user2 = models.ForeignKey('Person', models.DO_NOTHING, related_name= "user2")

    class Meta:
        db_table = 'friends'
        unique_together = (('user1', 'user2'),)


class Likes(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey('Person', models.DO_NOTHING, db_column='userid')
    food_type = models.CharField(max_length=30)
	
    def __str__(self):
        return self.food_type

    class Meta:
        db_table = 'likes'


class OpenAt(models.Model):
    restaurantid = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restaurantid')
    weekday = models.IntegerField(blank=True, null=True)
    open_time = models.IntegerField(blank=True, null=True)
    close_time = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'open_at'
        unique_together = (('restaurantid', 'weekday', 'open_time', 'close_time'),)


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    allow_strangers = models.BooleanField()
    has_meal_plan = models.BooleanField()
	
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'person'


class Restaurant(models.Model):
    restaurantid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
	
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'restaurant'

class Buildings(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'buildings'


class SoldBy(models.Model):
    food_type = models.CharField(max_length=30)
    restaurantid = models.ForeignKey(Restaurant, models.DO_NOTHING, db_column='restaurantid')
	
    def __str__(self):
        return self.food_type

    class Meta:
        db_table = 'sold_by'
        unique_together = (('restaurantid', 'food_type'),)
	

