"""
URL configuration for pratik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tempo import views 

urlpatterns = [
    
    # ----------------------------- Customer -----------------------------
    path('', views.home),
    path('save_account/', views.save_account),
    path('register/', views.register),
    path('register_now/', views.register_now),
    path('customers/', views.customers),
    path('edit_customers/', views.edit_customers),
    path('update_account/', views.update_account),
    path('do_login/', views.do_login),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # ---------------------------- Profile --------------------------------
    path('profile/', views.profile),
    path('dashboard/', views.dashboard),
    path('ready_dashboard/', views.ready_dashboard),
    
    # ---------------------------- Booking --------------------------------
    path('tempo/booking/booking/',views.booking),
    path('tempo/booking/booking_list/',views.booking_list),
    path('save_booking/',views.save_booking),
    path('update_booking/<int:id>/',views.update_booking),
    path('delete_booking/<int:id>/', views.delete_booking, name='delete_booking'),
    path('recover_booking/<int:id>/', views.recover_booking, name='recover_booking'),
    path('tempo/booking/deleted_bookings/', views.deleted_bookings, name='deleted_bookings'),
    
    # ----------------------------- Party ----------------------------------
    path('tempo/party/party/',views.party),
    path('tempo/party/party_list/',views.party_list),
    path('save_party/',views.save_party),
    path('delete_party/',views.delete_party),
    path('update_party/',views.update_party),
    path('edit_party/',views.edit_party),
    
    # ----------------------------- Vehicle --------------------------------
    path('tempo/vehicle/vehicle/',views.vehicle),
    path('tempo/vehicle/vehicle_list/',views.vehicle_list),
    path('tempo/master/master/',views.master),
    path('tempo/master/master_list/',views.master_list),
    path('save_vehicle/',views.save_vehicle),
    path('edit_vehicle/',views.edit_vehicle),
    path('update_vehicle/',views.update_vehicle),
    path('delete_vehicle/',views.delete_vehicle),
    
    # ------------------------------ Master ---------------------------------
    path('save_master/',views.save_master),
    path('edit_master/',views.edit_master),
    path('update_master/',views.update_master),
    path('delete_master/',views.delete_master),

]
