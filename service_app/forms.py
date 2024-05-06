import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from service_app.models import Login_view, Customer, Seles_Rentals, AppointmentSchedule, Sales_add, Complaints, Payments


class LoginRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = Login_view
        fields = ('username','password1','password2',)


class CustomerRegister(forms.ModelForm):

    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ("user",'status1')

class SellerRegister(forms.ModelForm):

    class Meta:
        model = Seles_Rentals
        fields = "__all__"
        exclude = ("user",'status2')





class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'



class ScheduleAdd(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput)
    end_time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = AppointmentSchedule
        fields = ('date', 'start_time','end_time','location')

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        date = cleaned_data.get("date")
        if start > end:
            raise forms.ValidationError("End Time should be greater than start Time.")

        if date < datetime.date.today():
            raise forms.ValidationError("Date can't be in the past")
        return cleaned_data




class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = ('feedback',)


class SalesRentalsForm(forms.ModelForm):
    class Meta:
        model = Sales_add
        fields = '__all__'
        exclude = ('user','status1')


class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'



