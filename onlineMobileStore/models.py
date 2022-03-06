from distutils.command.upload import upload
from django.db import models
from django.http import request

# Create your models here.
class Sale(models.Model):
    image = models.ImageField(null=True, blank=True)
    p_name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.p_name

class SpecialPrice(models.Model):
    image = models.ImageField(null=True, blank=True)
    p_name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.p_name

class NewPhone(models.Model):
    image = models.ImageField(null=True, blank=True)
    p_name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.p_name