from django.db import models

# Create your models here.

#from turtle import color
from django.db import models
#from asyncio.windows_events import NULL
from main_app.models import app_users,color_quantity,ceremony, priests, travel,permanent_Address,saved_Address

# Create your models here.


class gift_requests(models.Model):
    raised_by=models.ForeignKey(app_users,on_delete=models.CASCADE)
    product_associated=models.ForeignKey(color_quantity,on_delete=models.CASCADE)
    
    status_choices = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Waiting','Waiting')
        
    ]
    status=models.CharField(max_length=20,choices=status_choices,default='Waiting')

class product_cart(models.Model):
    product=models.ForeignKey(color_quantity,on_delete=models.CASCADE)
    customer=models.ForeignKey(app_users,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    payment_choices = [
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled','Cancelled'),
        ('Waiting','Waiting')
        
    ]
    payment_status=models.CharField(max_length=20,choices=payment_choices,default='Completed')

class ceremony_bookings(models.Model):
    ceremony_booked=models.ForeignKey(ceremony,on_delete=models.CASCADE)
    priest_selected=models.ForeignKey(priests,on_delete=models.CASCADE)
    date_scheduled=models.DateTimeField(null=True)
    payment_choices = [
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled','Cancelled'),
        ('Waiting','Waiting')
        
    ]
    payment_status=models.CharField(max_length=20,choices=payment_choices,default='Waiting')
    user_associated=models.ForeignKey(app_users,on_delete=models.CASCADE,null=True,default=None)

class yatra_bookings(models.Model):
    yatra=models.ForeignKey(travel,on_delete=models.CASCADE)
    yatra_user=models.ForeignKey(app_users,on_delete=models.CASCADE)
    status_choices=[
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        
        
    ]
    booking_status=models.CharField(max_length=20,choices=status_choices,default='Accepted')
    payment_choices = [
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled','Cancelled'),
        ('Waiting','Waiting')
        
    ]
    payment_status=models.CharField(max_length=20,choices=payment_choices,default='Waiting')

# in future the price for items will be dynamic so we are recording what was the price on that day when order was placed 
class prod_and_amount(models.Model):
    product=models.ForeignKey(color_quantity,on_delete=models.CASCADE)
    price=models.IntegerField()
    quantity=models.IntegerField(default=1)

# remove items from the cart when payment is done
class product_orders(models.Model):
    order_id=models.CharField(max_length=20,unique=True)
    amount=models.IntegerField()
    date=models.DateTimeField(null=True)
    done_by=models.ForeignKey(app_users,on_delete=models.CASCADE)
    products_associated=models.ManyToManyField(prod_and_amount)
    address=models.ForeignKey(saved_Address,on_delete=models.SET_NULL,null=True,default=None)
    payment_choices = [
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Cancelled','Cancelled'),
        ('Waiting','Waiting')
        
    ]
    payment_status=models.CharField(max_length=20,choices=payment_choices,default='Waiting')
    