from django.contrib.auth.models import AbstractUser
from django.db import models

#

class Login_view(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.ForeignKey(Login_view, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=50)
    phone_number=models.CharField(max_length=100)
    email = models.EmailField()
    status1=models.BooleanField(default=0)

    def __str__(self):
        return self.name



class Seles_Rentals(models.Model):
    user = models.ForeignKey(Login_view, on_delete=models.CASCADE, related_name='seller')
    name = models.CharField(max_length=50)
    Pancard_number = models.CharField(max_length=16)
    phone_number=models.CharField(max_length=100)
    email = models.EmailField()
    status2 = models.BooleanField(default=0)


class AppointmentSchedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=50 ,default="kerala")



class Appointment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointment')
    schedule = models.ForeignKey(AppointmentSchedule, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)


class Sales_add(models.Model):
    data= [

        ('Laptop', 'Laptop'),
        ('Tablets', 'Tablets'),


    ]
    TYPE = [
        ('Sale', 'Sale'),
        ('Rental', 'Rental'),
    ]
    user = models.ForeignKey(Login_view, on_delete=models.CASCADE)
    item = models.CharField(max_length=50, choices=data)
    type = models.CharField(max_length=50, choices=TYPE)
    location = models.CharField(max_length=50)
    description= models.TextField()
    rate = models.CharField(max_length=10)
    contact_no = models.CharField(max_length=100)
    pic = models.FileField(upload_to='pic/')
    status1 = models.BooleanField(default=0)
    quantity = models.PositiveIntegerField(default=0)


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sales_add, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10,default=0000000000)
    status = models.IntegerField(default=0)


class Complaints(models.Model):
    user = models.ForeignKey(Login_view, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    date = models.DateField(auto_now=True)
    reply = models.TextField(null=True, blank=True)

class Payments(models.Model):
    card_number = models.CharField(max_length=16)
    expiry = models.CharField(max_length=10)
    cvv = models.CharField(max_length=3)