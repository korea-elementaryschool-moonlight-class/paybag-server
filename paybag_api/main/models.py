from django.db import models

# Create your models here.
class User(models.Model) :
    email = models.EmailField()
    name = models.CharField(max_length = 20, null=True)
    password = models.CharField(max_length = 20)
    phone = models.CharField(max_length = 15)
    address = models.CharField(max_length = 100)
    count = models.IntegerField(default=0)
    stamp = models.IntegerField(default=0)
    isBlocked = models.BooleanField(default=False)
    uid = models.CharField(max_length = 20)
    coupon = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True)

class Card(models.Model) :
    card_num = models.CharField(max_length = 30)
    valid_thru = models.CharField(max_length = 5)
    name = models.CharField(max_length = 10, null=True)
    cvc = models.CharField(max_length = 3)
    card_pw = models.CharField(max_length = 2)
    uid = models.CharField(max_length = 20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True)

class Ecobag(models.Model) :
    uid = models.CharField(max_length = 20, null=True)
    status = models.CharField(max_length = 10, default="Having")
    lastMarket = models.CharField(max_length = 20, null=True)
    market = models.CharField(max_length = 20, null=True)
    eid = models.CharField(max_length = 20)
    note = models.CharField(max_length = 100, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True)

class History(models.Model) :
    uid = models.CharField(max_length = 20)
    eid = models.CharField(max_length = 20)
    rentMarket = models.CharField(max_length = 20, null=True)
    returnMarket = models.CharField(max_length = 20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True)

class Market(models.Model) :
    mid = models.CharField(max_length = 20)
    count = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    marketName = models.CharField(max_length = 100, null=True)
    address = models.CharField(max_length = 100)
    latitude = models.CharField(max_length = 20)
    longitude = models.CharField(max_length = 20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True)