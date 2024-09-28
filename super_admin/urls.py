from django.contrib import admin
from super_admin import views
from django.urls import path,include

urlpatterns = [
    path('manage/',views.manage_Admin ),
    path('create/',views.create_Admin ),
     path('toggle_ajax/<int:id>/',views.change_admin_status),
   
   # path('superadmin/',include('super_admin.urls'))
]