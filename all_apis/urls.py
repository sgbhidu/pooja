from django.contrib import admin
#import super_admin,main_app
from . import views
from django.urls import path,include
from django.conf import settings  
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('show_products',views.Products_list)
router.register('description',views.Color_quant_list)
router.register('products',views.Prdo_list)
router.register('ceremony',views.Ceremony_operations)
router.register('location',views.Location_lists)
router.register('travel',views.Travel_lists)
router.register('products_cart',views.Products_cart_lists)
router.register('gift_request',views.Gift_request_lists)
router.register('yatra_booking',views.Yatra_bookings)
router.register('ceremony_booking',views.Ceremony_bookings_lists)
#router.register('login',views.apilogin)

urlpatterns=[
    path('',include(router.urls)),
    path('one/',views.temp_view),
    path('login/',views.apilogin.as_view()),
    path('register/',views.apiRegister.as_view()),
    path('register/<int:pk>',views.apiRegister.as_view()),
    path('verify_otp/',views.verify_otp.as_view()),
    path('forgot_pwd/',views.forgot_pwd.as_view())
    #path('show_products/',views.Products_list.as_view()),
    #path('description/',views.Color_quant_list.as_view()),
    #path('products/',views.prdo_list.as_view()),
    #path('ceremony/',views.ceremony_operations.as_view()),
    #path('location/',views.location_lists.as_view()),
    #path('travel/',views.travel_lists.as_view()),
    #path('products_cart/',views.products_cart_lists.as_view()),
    #path('gift_request/',views.gift_request_lists.as_view()),
    #path('ceremony_booking/',views.ceremony_bookings_lists.as_view()),
    #path('yatra_booking/',views.yatra_bookings_lists.as_view())
]