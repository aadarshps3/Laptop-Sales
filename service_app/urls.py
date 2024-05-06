from django.urls import path

from service_app import views, admin_views, customer_views, sales_views

urlpatterns = [
 # path("",views.test,name="test"),
 # path("",views.landing_page,name="landing"),

 path('',views.RegistrationView.as_view(),name="view"),
 path('login_view', views.login_page, name="login_view"),
 path("admin_dashboard",views.admin_dashboard,name='admin_dashboard'),
 path("customer_dashboard", views.customer_dashboard, name='customer_dashboard'),
 path("seller_dashboard", views.seller_dashboard, name='seller_dashboard'),
 path("manager_dashboard", views.manager_dashboard, name='manager_dashboard'),

 path("logout_view", views.logout_view, name='logout_view'),

#admin
 path('customers',admin_views.customers,name='customers'),
 path('sellers',admin_views.sellers,name='sellers'),
 path("new",views.new,name="new"),
 path('schedule',admin_views.schedule_add,name='schedule'),
 path('schedule_view', admin_views.schedule, name='schedule_view'),
 path('schedule_delete/<int:id>/', admin_views.schedule_delete, name='schedule_delete'),
 path('adm_view_items',admin_views.adm_view_items,name='adm_view_items'),

 path('appointment_admin',admin_views.appointment_admin,name='appointment_admin'),
 path('approve_appointment/<int:id>/', admin_views.approve_appointment, name='approve_appointment'),
 path('reject_appointment/<int:id>/', admin_views.reject_appointment, name='reject_appointment'),

 path('feedbacks', admin_views.feedbacks, name='feedbacks'),
 path('reply_feedback/<int:id>/',admin_views.reply_feedback,name = 'reply_feedback'),


 #customer
 path("schedule_cus",customer_views.schedule_cus,name="schedule_cus"),
 path('take_appointment/<int:id>/', customer_views.take_appointment, name='take_appointment'),
 path('appointments', customer_views.appointments, name='appointments'),
 path('cus_view_items',customer_views.cus_view_items,name='cus_view_items'),
 path('Add_to_cart/<int:id>/',customer_views.Add_to_cart,name="Add_to_cart"),
 path('My_list',customer_views.My_list,name='My_list'),

 path("feedback",customer_views.feedback,name="feedback"),
 path("feedback_view", customer_views.feedback_view, name="feedback_view"),
 path("checkout/<int:id>/",customer_views.checkout,name='checkout'),
 path("checkout_rental/<int:id>/",customer_views.checkout_rental,name='checkout_rental'),


 #sales_rental
 path('add_sales_rental',sales_views.add_sales_rental, name='add_sales_rental'),
 path('view_items', sales_views.view_items, name='view_items'),
 path('instock/<int:id>/', sales_views.instock, name='instock'),
 path('out_of_stock/<int:id>/',sales_views.out_of_stock, name='out_of_stock'),
 path("sale_Bookings",sales_views.Bookings,name = "sale_Bookings"),
]