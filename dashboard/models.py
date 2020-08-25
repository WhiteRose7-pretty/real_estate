from django.db import models
from authentication.models import CustomUser


# Create your models here.
class RentType(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Pets(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Property(models.Model):
    owner = models.ForeignKey(CustomUser, null=True, related_name='properties', on_delete=models.CASCADE)
    photo = models.FileField()
    type = models.ForeignKey(RentType, null=True, related_name='properties', on_delete=models.CASCADE)
    pets = models.ManyToManyField(Pets, null=True, related_name='properties')
    beds = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    link = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.address + ',' + self.zipcode



