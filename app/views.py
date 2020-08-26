from django.shortcuts import render
from django.template.loader import render_to_string
from dashboard.models import Property, RentType, CustomUser
from .forms import PropertySearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers


def home(request):
    properties_all = Property.objects.all()
    search_form = PropertySearch(data=request.GET)

    # if location, filter by location
    location = request.GET.get('location', False)
    if location:
        location = location.split(',')[0]
        properties_all = properties_all.filter(zipcode__contains=location)

    # if lent type, filter by rent type
    lent_type = request.GET.getlist('rent_type')
    if len(lent_type):
        properties_all = properties_all.filter(type__pk__in=lent_type)

    # if pets, filter by pets
    pets = request.GET.getlist('pet')
    if len(pets):
        properties_all = properties_all.filter(pets__pk__in=pets)
    else:
        properties_all = properties_all.filter(pets=None)

    page = request.GET.get('page', 1)
    paginator_property = Paginator(properties_all, 4)

    try:
        properties = paginator_property.page(page)
    except PageNotAnInteger:
        properties = paginator_property.page(1)
    except EmptyPage:
        properties = paginator_property.page(paginator_property.num_pages)

    context = {
        'properties_all': properties_all,
        'properties': properties,
        'form': search_form
    }

    if request.is_ajax() and request.method == 'POST' and request.POST.get('command', False):
        ps_json = serializers.serialize('json', properties_all)
        return HttpResponse(ps_json, content_type='application/json')

    return render(request, 'app/home.html', context)
