from ctypes import addressof
#from msilib.schema import AdminExecuteSequence
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_slug
from django.utils.text import slugify
# Create your models here.

class permanent_Address(models.Model):
    address= models.CharField(max_length=200)
    landmark=models.CharField(max_length=200)
    pincode=models.IntegerField()
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    def __str__(self):
        return self.address



class app_users(models.Model):
    name=models.CharField(max_length=30)
    phone=models.IntegerField(null=True)
    alternate_phone=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    password=models.CharField(max_length=100)
    anniversary=models.DateField(null=True)
    date_of_birth=models.DateField(null=True)
    permanent_Address=models.OneToOneField(permanent_Address,on_delete=models.CASCADE,null=True)
    active=models.BooleanField(default=True)
    user_choices = [
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        
    ]
    user_type=models.CharField(max_length=10,choices=user_choices,default='Customer')
    last_otp=models.IntegerField(null=True)
    user_id=models.OneToOneField(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name


class saved_Address(models.Model):
    name=models.CharField(max_length=50,default="Dummy name")
    phone=models.CharField(max_length=50,default="1234567890")
    address= models.CharField(max_length=200)
    landmark=models.CharField(max_length=200)
    pincode=models.IntegerField()
    default=models.BooleanField(default=False)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    user=models.ForeignKey(app_users,on_delete=models.CASCADE)

'''added by admin these are pooja products'''
class pooja_products(models.Model):
    name=models.CharField(max_length=50)
    size=models.CharField(max_length=50)
    description=models.TextField()
    def __str__(self):
        return self.name

'''Colour with available quantity for pooja_products'''
class color_quantity(models.Model):
    color=models.CharField(max_length=20)
    quantity=models.IntegerField()
    price=models.IntegerField(default=0)
    photo=models.ImageField(verbose_name="photo",upload_to='images',null=True)
    product=models.ForeignKey(pooja_products,related_name="product",on_delete=models.CASCADE)
    slug=models.SlugField(unique=True,null=True)
    def __str__(self):
        return str(self.id)+" "+self.product.name+"("+self.color+")"
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            string=self.product.name+" "+self.color+" "+ self.product.size
            self.slug = generate_slug(string)
        return super().save(*args, **kwargs)
    
class product_ratings(models.Model):
    product=models.ForeignKey(color_quantity,on_delete=models.CASCADE)
    user=models.ForeignKey(app_users,on_delete=models.CASCADE)
    rating=models.IntegerField()
    reviews=models.TextField(null=True)
    def __str__(self):
        return self.product.product.name


# preists for ceremony that are added by admin and booked by customers
class priests(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    address=models.CharField(max_length=150)
    contact_number=models.IntegerField()
    def __str__(self):
        return self.name

#class ceremony(models.Model):
#    name=models.CharField(max_length=70)

class festivals(models.Model):
    name=models.CharField(max_length=30)
    start_date=models.DateField()
    end_date=models.DateField()
    duration=models.IntegerField()
    unit_choice=[('Hours','Hours'),('Minutes','Minutes'),('Days','Days')]
    duration_unit=models.CharField(max_length=30,choices=unit_choice,default='Days')
    def __str__(self):
        return self.name


class ceremony(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    price=models.IntegerField()
    photo=models.ImageField(null=True)
    available_priests=models.ManyToManyField(priests)
    materials_required=models.TextField(default=" ")
    procedure=models.TextField(default=" ")
    location=models.CharField(max_length=20,default="home")
    duration=models.IntegerField(default=1)
    unit_choice=[('Hours','Hours'),('Minutes','Minutes'),('Days','Days')]
    duration_unit=models.CharField(max_length=30,choices=unit_choice,default='Days')
    date=models.DateTimeField(null=True,default=None)
    date_fixed=models.BooleanField(default=True)
    festivals=models.ManyToManyField(festivals,null=True,blank=True,default=None)
    def __str__(self):
        return self.name

class location(models.Model):
    city=models.CharField(max_length=20)
    pin_code=models.IntegerField()
    def __str__(self):
        return self.city

class travel(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    price=models.IntegerField()
    locations_covered=models.ManyToManyField(location)
    photo=models.ImageField(null=True)

    def __str__(self):
        return self.name




