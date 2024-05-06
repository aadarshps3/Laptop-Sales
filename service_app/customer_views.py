from django.contrib import messages
from django.shortcuts import render, redirect

from service_app import models
from service_app.filters import PlaceFilter, AppointmentFilter
from service_app.forms import FeedbackForm, PaymentsForm
from service_app.models import AppointmentSchedule, Customer, Appointment, Sales_add, Cart, Complaints


def schedule_cus(request):
    s = AppointmentSchedule.objects.all()
    appointmentFilter = AppointmentFilter(request.GET, queryset=s)
    s=appointmentFilter.qs

    context = {
        'schedule': s,
        'appointmentFilter':appointmentFilter,

    }
    return render(request, 'customer/cus_schedule.html', context)


def take_appointment(request, id):
    schedule = AppointmentSchedule.objects.get(id=id)
    u = Customer.objects.get(user=request.user)
    appointment = Appointment.objects.filter(user=u , schedule=schedule)
    if appointment.exists():
        messages.info(request, 'You Have Already Requested Appointment for this Schedule')
        return redirect("schedule_cus")
    else:
        if request.method == 'POST':
            obj = Appointment()
            obj.user = u
            obj.schedule = schedule
            obj.save()
            messages.info(request, 'Appointment Booked Successfully')
            return redirect('appointments')
    return render(request, 'customer/take_appointment.html', {'schedule': schedule})



def appointments(request):
    u = Customer.objects.get(user=request.user)
    a = Appointment.objects.filter(user=u)
    return render(request, 'customer/cus_appointment.html', {'appointment': a})


def cus_view_items(request):

    data=Sales_add.objects.all()
    placeFilter = PlaceFilter(request.GET, queryset=data)
    data = placeFilter.qs

    return render(request,'customer/cus_items.html',{'data':data,"placeFilter":placeFilter})


def Add_to_cart(request, id):
    sale = Sales_add.objects.get(id=id)
    u = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        qty = int(request.POST.get("quantity", 0))
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        # Check if the requested quantity is available
        if qty > sale.quantity:
            return render(request, 'customer/no_stock.html')  # Redirect to no stock available page

        obj = Cart(user=u, sale=sale, quantity=qty, address=address, mobile=mobile)
        obj.save()

        # Update sale quantity
        sale.quantity -= qty
        sale.save()

        messages.info(request, 'Item added to My orders')
        return redirect('cus_view_items')

    return render(request, 'customer/bookings.html', {'schedule': sale})
#
# def Add_to_cart(request, id):
#     sale = Sales_add.objects.get(id=id)
#     u = Customer.objects.get(user=request.user)
#     # booking = Cart.objects.filter(user=u ,sale=sale)
#     # if booking.exists():
#     #     messages.info(request, 'You Have Already Booked this product')
#     #     return redirect("cus_view_items")
#     # else:
#     if request.method == 'POST':
#             obj = Cart()
#             obj.user = u
#             obj.sale = sale
#             qty = request.POST.get("quantity")
#             address = request.POST.get("address")
#             mobile = request.POST.get("mobile")
#             obj.quantity = qty
#             obj.address = address
#             obj.mobile = mobile
#             obj.save()
#             try:
#
#                 qty = int(qty)
#             except ValueError:
#
#                 qty = 0
#
#             # Now perform the subtraction operation
#
#             sale.quantity = sale.quantity - qty
#             print(sale.quantity)
#             sale.save()
#             messages.info(request, 'Item added to My orders')
#             return redirect('cus_view_items')
#     return render(request, 'customer/bookings.html', {'schedule': sale})


def My_list(request):
    u = request.user
    user = Customer.objects.get(user=u)
    ticket = Cart.objects.filter(user=user)
    return render(request, 'customer/my_ticket.html', {'ticket': ticket})


def feedback(request):
    form=FeedbackForm
    u= request.user

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request,"thank you for your feedback...!!!")
            return redirect('feedback_view')
    else:
        form = FeedbackForm()
    return render(request,'customer/add_feedback.html',{'form':form})


def feedback_view(request):

    u = Complaints.objects.filter(user=request.user)
    return render(request,"customer/feedback.html",{'feedback':u})

def checkout(request, id):
    n = Cart.objects.get(id=id)
    form = PaymentsForm()
    if request.method == 'POST':
        form = PaymentsForm(request.POST)
        if form.is_valid():
            form.save()



        n = Cart.objects.get(id=id)
        n.status = 1
        n.save()
        messages.info(request, 'Booking successful')
        return redirect('My_list')

    return render(request, 'customer/checkout.html', {'n': n,'form':form})

def checkout_rental(request, id):
    n = Appointment.objects.get(id=id)
    form = PaymentsForm()
    if request.method == 'POST':

            form = PaymentsForm(request.POST)
            if form.is_valid():
                form.save()
                n = Appointment.objects.get(id=id)
                n.status = 3
                n.save()
                messages.info(request, 'booking successful')
                return redirect('appointments')



    return render(request, 'customer/checkout.html', {'n': n,'form':form})