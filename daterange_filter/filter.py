# -*- coding: utf-8 -*-


'''
Has the filter that allows to filter by a date range.

'''
from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.translation import ugettext as _


class DateRangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(DateRangeForm, self).__init__(*args, **kwargs)

        self.fields['%s__gte' % field_name] = forms.CharField(
            label='', widget=TextInput(
                attrs={'class': 'vDateField', 'placeholder': _('From date')}), localize=True,
            required=False)

        self.fields['%s__lte' % field_name] = forms.CharField(
            label='', widget=TextInput(
                attrs={'class': 'vDateField', 'placeholder': _('To date')}), localize=True,
            required=False)


class DateRangeFilter(admin.filters.FieldListFilter):
    template = 'daterange_filter/filter.html'


    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super(DateRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        return DateRangeForm(data=self.used_parameters,
                             field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: bool(x[1]),
                                        self.form.cleaned_data.items()))
            return queryset.filter(**filter_params)
        else:
            return queryset


# register the filter
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.CharField), DateRangeFilter)
