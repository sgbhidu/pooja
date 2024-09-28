from django.contrib import admin
from customers import views
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('home',views.homepage),
    path('view_products',views.view_products),
    path('view_gifts',views.view_gifts),
    path('request_gift/<int:pid>',views.add_gift_request),
    path('view_gift_details/<slug:slug>',views.view_gift_details),
    path('view_products_cart',views.view_products_cart),
    path('remove_cart_item/<slug:slug>',views.remove_cart_item),
    path('view_ceremonies',views.view_ceremonies),
    path('product_checkout',views.product_checkout),
    path('initiate_payment/<str:order_type>',views.initiate_payment),
    path('schedule_ceremony/<int:pid>',views.schedule_ceremony),
    path('view_ceremony_bookings',views.view_ceremony_bookings),
    path('view_gift_requests',views.view_gift_requests),
    path('view_yatras',views.view_yatras),
    path('book_yatra/<int:pid>',views.book_yatra),
    path('view_yatra_bookings',views.view_yatra_bookings),
    path('handlerequest/',views.handlerequest),
    path('payment_success/<str:order_type>/<str:order_id>',views.payment_success),
    path('payment_cancel',views.payment_cancel),
    path('order_details/<str:order_id>',views.view_order),
    path('all_orders/',views.order_history),
    path('webhook/',views.stripe_webhook)

]