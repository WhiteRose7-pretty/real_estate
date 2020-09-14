from django.db import models
from authentication.models import CustomUser
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


# Create your models here.
class RentType(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Pets(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class RealEstate(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    owner = models.ForeignKey(CustomUser, null=True, related_name='properties', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images')
    photo_url = models.URLField()
    type = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(RentType, null=True, related_name='properties_of_type', on_delete=models.CASCADE)
    pets = models.BooleanField(null=True, blank=True, default=False)
    beds = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    link = models.CharField(max_length=255, null=True)
    likes = models.ManyToManyField(CustomUser, related_name='like_property', null=True)
    lat = models.DecimalField(max_digits=13, decimal_places=10, default=0, null=True)
    lng = models.DecimalField(max_digits=13, decimal_places=10, default=0, null=True)

    def __str__(self):
        return str(self.pk) + '-' + self.address + ',' + self.zipcode

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo_url and not self.photo:
            if self.photo_url and not self.photo:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.photo_url).read())
                img_temp.flush()
                self.photo.save(f"image_{self.pk}", File(img_temp))
            self.save()




