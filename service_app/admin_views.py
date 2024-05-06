from django.contrib import messages
from django.shortcuts import redirect,render

from service_app.forms import ScheduleAdd
from service_app.models import AppointmentSchedule, Appointment, Sales_add, Complaints, Customer, Seles_Rentals


def customers(request):
    data = Customer.objects.all()
    return render(request,"admin/customerlist.html",{"data":data})

def sellers(request):
    data = Seles_Rentals.objects.all()
    return render(request,"admin/sellelist.html",{"data":data})


def schedule_add(request):
    form = ScheduleAdd()
    if request.method == 'POST':
        form = ScheduleAdd(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, ' Schedule Added Successfully')
            return redirect('schedule_view')
    else:
        form = ScheduleAdd()
    return render(request, 'admin/schedule_add.html', {'form': form})



def schedule(request):
    n = AppointmentSchedule.objects.all()

    context = {
        'schedule': n,

    }
    return render(request, 'admin/schedule_view.html', context)


def schedule_delete(request, id):
    n = AppointmentSchedule.objects.get(id=id)
    if request.method == 'POST':
        n.delete()
        messages.info(request, 'Schedule Deleted Successfully')
        return redirect('schedule_view')




def appointment_admin(request):
    p = Appointment.objects.all()

    context = {
        'appointment': p,

    }
    return render(request, 'admin/appointment.html', context)


def approve_appointment(request, id):
    n = Appointment.objects.get(id=id)
    n.status = 1
    n.save()
    messages.info(request, 'Appointment  Confirmed')
    return redirect('appointment_admin')


def reject_appointment(request, id):
    n = Appointment.objects.get(id=id)
    n.status = 2
    n.save()
    messages.info(request, 'Appointment Rejected')
    return redirect('appointment_admin')


def adm_view_items(request):

    data=Sales_add.objects.all()

    return render(request,'admin/new.html',{'data':data})



def feedbacks(request):
    n = Complaints.objects.all()
    return render(request,'admin/feedbacks.html',{'feedbacks':n})

def reply_feedback(request,id):
    feedback = Complaints.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        feedback.reply = r
        feedback.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('feedbacks')
    return render(request, 'admin/admin_feedback.html', {'feedback': feedback})