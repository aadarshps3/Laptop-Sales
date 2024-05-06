from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

# # Create your views here.
# def test(request):
#     return render(request,"home.html")
from django.views import View

from service_app.forms import CustomerRegister, LoginRegister, SellerRegister


# def landing_page(request):
#     return render(request,"index.html")



def admin_dashboard(request):
    return render(request,'admin_dash.html')

def customer_dashboard(request):
    return render(request,'customer_dash.html')

def seller_dashboard(request):
    return render(request,'seller_dash.html')

def manager_dashboard(request):
    return render(request,'rental_manager.html')




#
class RegistrationView(View):
    def get(self, request):
        user = LoginRegister()
        customer_form = CustomerRegister()
        seller_form = SellerRegister()

        return render(request, 'index.html', {"user": user, "customer_form": customer_form,
                                            "seller_form": seller_form})

    def post(self, request):
        user = LoginRegister(request.POST)
        customer_form = CustomerRegister(request.POST)
        seller_form = SellerRegister(request.POST)




        if user.is_valid() and seller_form.is_valid():
            a = user.save(commit=False)
            a.is_seller = True
            a.save()
            user1 = seller_form.save(commit=False)
            user1.user = a
            user1.save()
            return redirect('login_view')


        elif user.is_valid() and customer_form.is_valid():
            a = user.save(commit=False)
            a.is_customer = True
            a.save()
            user1 = customer_form.save(commit=False)
            user1.user = a
            user1.save()
            return redirect('login_view')

        else:
            messages.info(request, 'Registration Failed...Password must contain at least 8 characters including alphabets and digits..')

        return render(request, 'index.html', {"user": user, "customer_form": customer_form,
                                            "seller_form": seller_form})
#
#
#
#
#
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        print(username)
        password = request.POST.get('pass')
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect('appointment_admin')
            elif user.is_customer:

                return redirect('cus_view_items')

            elif user.is_seller:

                return redirect('sale_Bookings')




        else:
            messages.info(request, 'Invalid Credentials')
    return render(request,'login_page.html')



def new(request):
    return render(request,'admin/new.html')



def logout_view(request):
    logout(request)
    return redirect('login_view')