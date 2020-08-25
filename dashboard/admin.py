from django.contrib import admin
from .models import Property, RentType, Pets

# Register your models here.
admin.site.register(Property)
admin.site.register(RentType)
admin.site.register(Pets)

