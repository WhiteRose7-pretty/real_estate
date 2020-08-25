from django import forms
from dashboard.models import RentType, Pets

BED_CHOICE = (
    ('0', 'All beds'),
    ('1', '1+ beds'),
    ('2', '2+ beds'),
    ('3', '3+ beds'),
)


class PropertySearch(forms.Form):
    rent_type = forms.ModelChoiceField(queryset=RentType.objects.all(),
                                       required=False,
                                       empty_label=None,
                                       widget=forms.SelectMultiple(attrs={'class': 'form-control selectpicker',
                                                                          'data-style': "btn-selectpicker",
                                                                          'data-selected-text-format': "count &gt; 1",
                                                                          'title': 'All Rent Type'}))
    pet = forms.ModelChoiceField(queryset=Pets.objects.all(),
                                 empty_label=None,
                                 required=False,
                                 widget=forms.SelectMultiple(attrs={'class': 'form-control selectpicker',
                                                                    'data-style': "btn-selectpicker",
                                                                    'data-selected-text-format': "count &gt; 2",
                                                                    'title': 'No Pet Allowed'}))
    bed = forms.ChoiceField(choices=BED_CHOICE,
                            required=False,
                            widget=forms.Select(attrs={'class': 'form-control selectpicker',
                                                       'data-style': "btn-selectpicker"}))

    price_min = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'slider-snap-input-from'}), required=False)
    price_max = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'slider-snap-input-to'}), required=False, )
    search_text = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Keywords'}),  required=False)
    near_check = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
                                    required=False)
