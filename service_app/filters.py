import django_filters
from django import forms
from django_filters import CharFilter


from service_app.models import Sales_add, AppointmentSchedule


class PlaceFilter(django_filters.FilterSet):
    location = CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search location ', 'class': 'form-control'}))

    class Meta:
        model = Sales_add
        fields = ('location',)


class AppointmentFilter(django_filters.FilterSet):
    location = CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search location ', 'class': 'form-control'}))

    class Meta:
        model = AppointmentSchedule
        fields = ('location',)