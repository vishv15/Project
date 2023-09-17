from django.db import models

# Create your models here.
class publisher(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    company = models.CharField(max_length=64)
    website = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="pics")
    
class admin(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    
class City(models.Model):
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    pincode = models.IntegerField()
    
class Event(models.Model):
    publisherid = models.IntegerField()
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="pics")
    city = models.CharField(max_length=255)
    eventtype = models.IntegerField()
    categoryid = models.IntegerField()
    
class EventDetail(models.Model):
    eventid = models.IntegerField()
    event_date = models.DateField()
    event_time = models.CharField(max_length=12)
    duration = models.IntegerField()    
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    contactno =models.CharField(max_length=16)
    contactperson = models.CharField(max_length=64)
    is_canceled = models.IntegerField()

class EventPrice(models.Model):
    eventid = models.IntegerField()
    title =  models.CharField(max_length=32)
    price = models.IntegerField()

class Review(models.Model):
    eventid = models.IntegerField()
    registeruser_id = models.IntegerField()
    title =  models.CharField(max_length=32)
    detail =  models.CharField(max_length=128)
    rating =  models.IntegerField()
    
class RegisterUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=32)