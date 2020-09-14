# from celery.task.schedules import crontab
# from celery.decorators import periodic_task

import pickle
import re
from dashboard.models import RealEstate, RentType
from celery import shared_task
import json
from googlegeocoder import GoogleGeocoder


@shared_task
def update_data(aa, min_index, max_index):
    i = 0
    jdata = json.loads(aa)
    for item in jdata:
        print(i)
        i = i + 1
        if i <= min_index:
            continue
        if i > max_index:
            break
        estate = RealEstate()
        estate.type = item['type']
        if item['type'] == 'Townhouse' or item['type'] == 'Townhome':
            town_house = RentType.objects.filter(name='Townhome').first()
            estate.category = town_house
        elif item['type'] == 'Single Family Home':
            single_home = RentType.objects.filter(name='Single Family Home').first()
            estate.category = single_home
        else:
            apartment = RentType.objects.filter(name='Apartment/Condo/Loft').first()
            estate.category = apartment
        if 'not' in item['pets']:
            estate.pets = False
        else:
            estate.pets = True

        try:
            estate.beds = re.search(r'\d+', item['beds']).group()
        except:
            estate.beds = 0

        try:
            estate.baths = re.search(r'\d+', item['baths']).group()
        except:
            estate.baths = 0

        try:
            # estate.price = re.findall(r'^\D*(\d+)', item['price'])
            item['price'] = item['price'].replace(",", "")
            estate.price = re.search(r'\d+', item['price']).group()

        except:
            estate.price = 0

        estate.address = item['address']
        estate.zipcode = item['zip_code']
        estate.link = item['link']

        estate.photo_url = item['photo']
        try:
            estate.save()
        except:
            print('can not save')


@shared_task
def delete_data(data):
    for item in data:
        item.delete()


@shared_task
def update_geo_code(min_index, max_index):
    temp_properties = RealEstate.objects.order_by('-id').all()
    i = 0
    geocoder = GoogleGeocoder("AIzaSyD8A1j9FdYG0tGsPwf8Sa8aBOVkjHvGPws")
    for item in temp_properties:
        i = i + 1
        if i <= min_index:
            continue
        if i > max_index:
            break
        real_address = item.address + ',' + item.zipcode
        try:
            search = geocoder.get(real_address)
        except:
            item.delete()
            continue
        print(i)
        print(search[0].geometry.location.lat)
        item.lat = search[0].geometry.location.lat
        print(search[0].geometry.location.lng)
        item.lng = search[0].geometry.location.lng
        try:
            item.save()
        except:
            item.delete()




