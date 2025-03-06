from django.urls import path
from .import views

urlpatterns=[path('',views.landing, name='landing'),
             path('register/',views.registration,name='registration'),
             path('login/',views.login,name='login'),
             path('dashboard/',views.dashboard,name='dashboard'),
             path('adminlogin/',views.admin_login,name='admin_login'),
             path('admindashboard',views.admin_dashboard,name='admin_dashboard'),
             path('logout/',views.logout1,name='logout1'),
             path('unverifiedusers/',views.unverifiedusers,name='unverifiedusers'),
             path('unverifiedlands/',views.unverifiedlands,name='unverifiedlands'),
             
             path('unverifyuser/',views.unverifyuser,name='unverifyuser'),
             path('unverifyland/',views.unverifyland,name='unverifyland'),
             path('registerland/',views.registerland,name='registerland'),
             
             path('user_details/<id>/',views.user_details,name='user_details'),
             path('land_details/<id>/',views.land_details,name='land_details'),
             ]