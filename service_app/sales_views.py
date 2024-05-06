from django.contrib import messages
from django.shortcuts import redirect, render

from service_app.forms import SalesRentalsForm
from service_app.models import Sales_add, Seles_Rentals, Cart


def add_sales_rental(request):
    if request.method == 'POST':
        u = request.user
        print(u)
        form = SalesRentalsForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            obj=form.save(commit=False)
            print(obj)
            obj.user=u
            obj.save()
            return redirect('view_items')
    else:
        form = SalesRentalsForm()
    return render(request, 'sales/sale_rental.html', {'form': form})


def view_items(request):
    u = request.user
    data=Sales_add.objects.filter(user=u)
    print(data)
    return render(request,'sales/items.html',{'data':data})


def instock(request, id):
    n = Sales_add.objects.get(id=id)
    print(n)
    n.status1 = 0
    n.save()
    messages.info(request, 'Status changed to Available')
    return redirect('view_items')


def out_of_stock(request, id):
    n = Sales_add.objects.get(id=id)
    print(n)
    n.status1 = 1
    n.save()
    messages.info(request, 'Status changed to Out of stock')
    return redirect('view_items')



def Bookings(request):
    u = request.user
    # user = Seles_Rentals.objects.get(user=u)
    # print(user)
    ticket = Cart.objects.filter(sale__user=u)
    print(ticket)
    return render(request,'sales/my_ticket.html', {'ticket': ticket})



