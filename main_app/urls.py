from django.contrib import admin
from main_app import views
from django.urls import path,include
from django.conf import settings  
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',views.userlogin),
    path('signup/', views.register),
   path('login/',views.userlogin),
   path('logout/',views.user_logout),
  path('landingpage/',views.landingpage),
   path('verifyOTP/',views.verify_otp),
   path('resendotp/',views.resend_otp),
   path('adduserdetails/',views.add_user_details),
   path('adminn/manage/',views.show_admin),
   path('adminn/add_product',views.add_product),
   path('adminn/add_gifts',views.add_gifts),
   path('adminn/view_products',views.view_product_admin),
   path('adminn/edit_product/<slug:slug>',views.edit_product_admin),
   path('adminn/delete_product/<int:pid>',views.delete_product_admin),
   path('adminn/view_ceremonies',views.view_ceremonies_admin),
   path('adminn/edit_ceremony/<int:pid>',views.edit_ceremony_admin),
   path('adminn/delete_ceremony/<int:pid>',views.delete_ceremony_admin),
   path('adminn/add_ceremony',views.add_ceremony),
   path('adminn/add_priest',views.add_priest),
   path('adminn/add_location',views.add_location_admin),
   path('adminn/add_yatra',views.add_yatra_admin),
   path('adminn/delete_yatra/<int:pid>',views.delete_yatra_admin),
   path('adminn/edit_yatra/<int:pid>',views.edit_yatra_admin),
   path('adminn/view_yatras',views.view_yatra_Admin),
   path('adminn/view_gift_requests',views.view_gift_requests),
   path('adminn/accept_gift_request/<int:pid>',views.accept_gift_request),
   path('adminn/reject_gift_request/<int:pid>',views.reject_gift_request),

]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
