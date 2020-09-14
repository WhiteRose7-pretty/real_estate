from django.contrib import admin
from .models import RealEstate, RentType, Pets

# Register your models here.
admin.site.register(RealEstate)
admin.site.register(RentType)
admin.site.register(Pets)

