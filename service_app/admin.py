from django.contrib import admin

from service_app import models

admin.site.register(models.Login_view)

admin.site.register(models.Customer)

admin.site.register(models.Sales_add)

admin.site.register(models.AppointmentSchedule)

admin.site.register(models.Cart)