from django import forms
from dashboard.models import RentType, Pets
from .models import Preference

BED_CHOICE = (
    ('0', 'ALL BEDS'),
    ('1', '1+ BEDS'),
    ('2', '2+ BEDS'),
    ('3', '3+ BEDS'),
)

BATH_CHOICE = (
    ('0', 'ALL BATHS'),
    ('1', '1+ BATHS'),
    ('2', '2+ BATHS'),
    ('3', '3+ BATHS'),
)

PET_CHOICE = (
    ('', 'Pets'),
    ('True', 'Pet Allowed'),
    ('False', 'No Pets'),
)


class PropertySearch(forms.Form):
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control auto-complete', 'id': 'search_location', 'placeholder': 'Enter your location'}),
        required=False, )

    rent_type = forms.ModelChoiceField(queryset=RentType.objects.all(),
                                       required=False,
                                       empty_label=None,
                                       widget=forms.SelectMultiple(attrs={'class': 'form-control selectpicker',
                                                                          'data-style': "btn-selectpicker",
                                                                          'data-selected-text-format': "count &gt; 1",
                                                                          'title': 'All Rent Types'}))
    pet = forms.ChoiceField(choices=PET_CHOICE,
                            required=False,
                            widget=forms.Select(attrs={'class': 'form-control selectpicker',
                                                       'data-style': "btn-selectpicker"}))
    bed = forms.ChoiceField(choices=BED_CHOICE,
                            required=False,
                            widget=forms.Select(attrs={'class': 'form-control selectpicker ',
                                                       'data-style': "btn-selectpicker"}))

    bath = forms.ChoiceField(choices=BATH_CHOICE,
                             required=False,
                             widget=forms.Select(attrs={'class': 'form-control selectpicker mt-1',
                                                        'data-style': "btn-selectpicker"}))

    price_min = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'id_price_min'}), required=False)
    price_max = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'id_price_max', 'value': '30000'}),
                                required=False, )
    search_text = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Advanced Filter'}), required=False)
    near_check = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
                                    required=False)


class AutoComplete(forms.Form):
    autocomplete = forms.ModelChoiceField(queryset=Preference.objects.all(), empty_label=None,
                                          widget=forms.SelectMultiple())


