from django.shortcuts import render
from django.template.loader import render_to_string
from dashboard.models import Property, RentType, CustomUser
from .forms import PropertySearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse


def home(request):
    properties_all = Property.objects.all()
    search_form = PropertySearch()

    page = request.GET.get('page', 1)
    paginator_property = Paginator(properties_all, 2)

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

    if request.is_ajax() and request.GET.get('search_', False):
        rendered = render_to_string('app/basic/content.html', context, request)
        return JsonResponse(rendered, safe=False)
    return render(request, 'app/home.html', context)
