# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class BusyAt(models.Model):
    userid = models.ForeignKey('Person', models.DO_NOTHING, db_column='userid', unique=True)
    location = models.TextField()  # This field type is a guess.
    weekday = models.TextField()  # This field type is a guess.
    timeblock = models.DateTimeField()

    class Meta:
        db_table = 'busy_at'
        unique_together = (('userid', 'weekday', 'timeblock'),)

class Friends(models.Model):
    user1 = models.ForeignKey('Person', models.DO_NOTHING, unique=True, related_name = "user1")
    user2 = models.ForeignKey('Person', models.DO_NOTHING, unique=True, related_name= "user2")

    class Meta:
        db_table = 'friends'
        unique_together = (('user1', 'user2'),)


class Likes(models.Model):
    userid = models.ForeignKey('Person', models.DO_NOTHING, db_column='userid', primary_key=True)
    food_type = models.CharField(max_length=30)

    class Meta:
        db_table = 'likes'


class OpenAt(models.Model):
    restaurantid = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restaurantid', unique=True)
    weekday = models.TextField()  # This field type is a guess.
    timeblock = models.DateTimeField()

    class Meta:
        db_table = 'open_at'
        unique_together = (('restaurantid', 'weekday', 'timeblock'),)


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    allow_strangers = models.BooleanField()
    has_meal_plan = models.BooleanField()

    class Meta:
        db_table = 'person'


class Restaurant(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'restaurant'


class SoldBy(models.Model):
    restaurantid = models.ForeignKey(Restaurant, models.DO_NOTHING, db_column='restaurantid', unique=True)
    food_type = models.CharField(max_length=30)

    class Meta:
        db_table = 'sold_by'
        unique_together = (('restaurantid', 'food_type'),)
