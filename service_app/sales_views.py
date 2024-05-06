from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

import xlsxwriter
from io import BytesIO

from service_app.forms import SalesRentalsForm, RentalsForm
from service_app.models import Sales_add, Seles_Rentals, Cart, Rentals_add


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

###########################################

def add_rental(request):
    if request.method == 'POST':
        u = request.user
        print(u)
        form = RentalsForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            obj=form.save(commit=False)
            print(obj)
            obj.user=u
            obj.save()
            return redirect('view_items_rental')
    else:
        form = RentalsForm()
    return render(request, 'sales/add_rental.html', {'form': form})


def view_items_rental(request):
    u = request.user
    data=Rentals_add.objects.filter(user=u)
    print(data)
    return render(request,'sales/view_items_rental.html',{'data':data})


def instock_rentals(request, id):
    n = Rentals_add.objects.get(id=id)
    print(n)
    n.status1 = 0
    n.save()
    messages.info(request, 'Status changed to Available')
    return redirect('view_items_rental')


def out_of_stock_rentals(request, id):
    n = Rentals_add.objects.get(id=id)
    print(n)
    n.status1 = 1
    n.save()
    messages.info(request, 'Status changed to Out of stock')
    return redirect('view_items_rental')



def Bookings(request):
    u = request.user
    # user = Seles_Rentals.objects.get(user=u)
    # print(user)
    ticket = Cart.objects.filter(sale__user=u)
    print(ticket)
    return render(request,'sales/my_ticket.html', {'ticket': ticket})


def report_form(request):
    return render(request, 'sales/report_form.html')


def generate_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Fetch sales data within the specified date range
        sales_data = Sales_add.objects.filter(posted_date__range=[start_date, end_date])

        # Fetch rentals data within the specified date range
        rentals_data = Rentals_add.objects.filter(posted_date__range=[start_date, end_date])

        # Create a new Excel workbook and add a worksheet
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Sales and Rentals Report')

        # Write headers
        headers = ['Item', 'Location', 'Description', 'Rate/Monthly Rent', 'Contact No', 'Status', 'Quantity',
                   'Posted Date', 'Listing Type']  # Include a column for listing type
        worksheet.write_row(0, 0, headers)

        # Write sales data
        row = 1
        for sale in sales_data:
            worksheet.write_row(row, 0,
                                [sale.item, sale.location, sale.description, sale.rate, sale.contact_no, sale.status1,
                                 sale.quantity, sale.posted_date, sale.listing_type])  # Include the listing type
            row += 1

        # Write rentals data
        for rental in rentals_data:
            worksheet.write_row(row, 0, [rental.item, rental.location, rental.description, rental.monthly_rent,
                                         rental.contact_no, rental.status1, rental.quantity, rental.posted_date,
                                         rental.listing_type])  # Include the listing type
            row += 1

        # Close the workbook
        workbook.close()

        # Set response headers to indicate an Excel file attachment
        response = HttpResponse(output.getvalue(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'

        return response

    else:
        return HttpResponse("Invalid Request")


def download_report(request, start_date, end_date, listing_type):
    # Determine the model based on the listing type
    if listing_type == 'sale':
        model = Sales_add
    elif listing_type == 'rental':
        model = Rentals_add
    else:
        return HttpResponse("Invalid listing type")

    # Fetch data within the specified date range and type
    data = model.objects.filter(posted_date__range=[start_date, end_date])

    # Create a new Excel workbook and add a worksheet
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Sales and Rentals Report')

    # Write headers
    headers = ['Item', 'Location', 'Description', 'Rate/Monthly Rent', 'Contact No', 'Status', 'Quantity',
               'Posted Date']
    worksheet.write_row(0, 0, headers)

    # Write data
    row = 1
    for item in data:
        if listing_type == 'sale':
            worksheet.write_row(row, 0,
                                [item.item, item.location, item.description, item.rate, item.contact_no, item.status1,
                                 item.quantity, item.posted_date])
        elif listing_type == 'rental':
            worksheet.write_row(row, 0, [item.item, item.location, item.description, item.monthly_rent, item.contact_no,
                                         item.status1, item.quantity, item.posted_date])
        row += 1

    # Close the workbook
    workbook.close()

    # Set response headers to indicate an Excel file attachment
    response = HttpResponse(output.getvalue(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'

    return response