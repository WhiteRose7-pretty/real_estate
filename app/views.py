from django.shortcuts import render
from django.template.loader import render_to_string
from dashboard.models import RealEstate, RentType, CustomUser
from .forms import PropertySearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
from .tasks import update_data, update_geo_code
import pickle
import json
from googlegeocoder import GoogleGeocoder



def home(request):
    # update_data()

    properties_all = RealEstate.objects.order_by('-id').all()

    # delete_data(properties_all)
    search_form = PropertySearch(data=request.GET)

    # if location, filter by location
    location = request.GET.get('location', False)
    if location:
        location = location.split(',')[0]
        properties_all = properties_all.filter(zipcode__contains=location)

    # if lent type, filter by rent type
    lent_type = request.GET.getlist('rent_type')
    if len(lent_type):
        properties_all = properties_all.filter(category_id__in=lent_type)

    # if pets, filter by pets
    pets = request.GET.get('pet', '')
    if not pets == '':
        properties_all = properties_all.filter(pets=pets)

    # bed filter
    beds = request.GET.get('bed', 0)
    properties_all = properties_all.filter(beds__gte=beds)

    # bath filter
    baths = request.GET.get('bath', 0)
    properties_all = properties_all.filter(baths__gte=baths)

    # price filter
    price_min = int(request.GET.get('price_min', 0))
    price_max = int(request.GET.get('price_max', 30000))
    properties_all = properties_all.filter(price__range=(price_min, price_max))

    # text filter
    search_text = request.GET.get('search_text', False)
    if search_text:
        properties_all = properties_all.filter(address__contains=search_text)

    print(len(properties_all))

    page = request.GET.get('page', 1)
    paginator_property = Paginator(properties_all, 12)

    try:
        properties = paginator_property.page(page)
    except PageNotAnInteger:
        properties = paginator_property.page(1)
    except EmptyPage:
        properties = paginator_property.page(paginator_property.num_pages)

    # Add is_liked field to video
    for property_item in properties:
        if not property_item.photo:
            property_item.delete()

        if property_item.beds == 0:
            property_item.delete()

        if property_item.baths == 0:
            property_item.delete()

        property_item.is_liked = ''
        if request.user.is_authenticated:
            if property_item.likes.filter(id=request.user.id).exists():
                property_item.is_liked = 'liked'
        property_item.save()

    context = {
        'properties_all': properties_all,
        'properties': properties,
        'form': search_form
    }

    if request.is_ajax() and request.method == 'POST' and request.POST.get('command', False):
        ps_json = serializers.serialize('json', properties_all)
        return HttpResponse(ps_json, content_type='application/json')

    if request.is_ajax() and page == '1':
        html_data = render_to_string('app/basic/content.html', context, request)
        return JsonResponse(html_data, safe=False)

    return render(request, 'app/home.html', context)


def property_likes(request):
    property = RealEstate.objects.get(pk=request.POST.get('id', False))
    is_liked = False
    if property.likes.filter(id=request.user.id).exists():
        property.likes.remove(request.user)
        is_liked = False
    else:
        property.likes.add(request.user)
        is_liked = True
    likes_counts = len(property.likes.all())
    json_output = {
        'is_liked': is_liked,
        'counts': likes_counts
    }
    return JsonResponse(json_output)


def obj_dict(obj):
    return obj.__dict__


def update(request):

    command = 'geo_code'
    if command == 'geo_code':
        update_geo_code.delay(4620, 8000)

    elif command == 'update':
        with open('app/property_CA_1.txt', "rb+") as fp:
            aa = pickle.load(fp)
            json_string = json.dumps(aa, default=obj_dict)
            update_data.delay(json_string, 6000, 8000)
    return HttpResponseRedirect("/")


