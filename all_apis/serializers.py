from rest_framework import serializers
from main_app.models import app_users,pooja_products,color_quantity,priests,ceremony,location,travel
from customers.models import ceremony_bookings,product_cart,gift_requests,yatra_bookings
from django.contrib.auth.models import User
from django.core.mail import send_mail
import math,random
class otp_serializer(serializers.Serializer):
    otp=serializers.IntegerField()
    def create(self,validated_data):
        #print(self.request.user)
        #print(validated_data)
        return "yes"
    
# here we take email from user and send otp on the email #
class forgot_password_serializer(serializers.Serializer):
    email=serializers.EmailField()
    def create(self,validated_data):
        return True

class app_users_serializer(serializers.ModelSerializer):
    class Meta:
        model=app_users
        fields=['id','name','phone','user_type','email','password']

    def create(self,validated_data):
        username=validated_data['email']
        password=validated_data['password']
        user_id=User.objects.create(username=username)
        user_id.set_password(password)
        user_id.save()
        app_user_obj=app_users.objects.create(**validated_data)
        app_user_obj.user_type='Customer'
        app_user_obj.active=False
        app_user_obj.user_id=user_id
        digits = "0123456789"
        OTP = ""
 
        for i in range(4) :
            OTP += digits[math.floor(random.random() * 10)]
        msg="HI There , the otp to verify your account is :- " + str(OTP)
        send_mail("Verify your Account",msg,'djangodemo72@gmail.com',[username])
        app_user_obj.last_otp=OTP
        app_user_obj.save()

        return app_user_obj
    def update(self,user_obj,validated_data):
        #user_obj=app_users.objects.get(id=pk)
        #print(self.email)
        #if(validated_data['name']):
        #    user_obj.name=validated_data['name']
        
        print(self)
        print(validated_data)
        for attr, value in validated_data.items():
            if(attr=='password'):
                user_obj.user_id.set_password(value)
                user_obj.user_id.save()
                user_obj.save()
            elif(attr=='email'):
                continue
            setattr(user_obj, attr, value)
        user_obj.save()
        #user_obj.save()
        return user_obj


class login_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    def create(self,validated_data):
        print(validated_data)

class seperate_pd_serializer(serializers.ModelSerializer):
    class Meta:
        model=pooja_products
        fields='__all__'
class pooja_serializer(serializers.ModelSerializer):
    #photo=serializers.ImageField(required=False)
    product=seperate_pd_serializer(read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
         write_only=True, queryset=pooja_products.objects.all()
    )
    class Meta:
        model=color_quantity
        #fields= ['color','quantity','price','photo','productt']
        fields='__all__'
    def create(self,validated_data):
        s=validated_data.pop('product_ids')
        print("working")
        print(validated_data)
        variant=color_quantity.objects.create(**validated_data,product=s)
        return variant
class product_serializer(serializers.ModelSerializer):
    productt=pooja_serializer(many=True) 
    class Meta:
        model=pooja_products
        fields= '__all__'
    
    def create(self,validated_data):
        pooja_data=validated_data.pop('productt')
        print(validated_data)
        #print(**validated_data)
        print(pooja_data)
        querry=pooja_products.objects.filter(name=validated_data['name'],size=validated_data['size'])
        if(len(querry)==1):
            productt=querry.first()
        else:
            productt=pooja_products.objects.create(**validated_data)
        print(productt)
        for data in pooja_data:
           color_quantity.objects.create(product=productt,**data)
        return productt
    

class priest_serializer(serializers.ModelSerializer):
    class Meta:
        model=priests
        fields='__all__'

class ceremony_serializer(serializers.ModelSerializer):
    available_priests=priest_serializer(read_only=True,many=True)
    available_priests_ids=serializers.PrimaryKeyRelatedField(many=True,write_only=True, queryset=priests.objects.all())
    class Meta:
        model=ceremony
        fields='__all__'
    def create(self,validated_data):
        
        print(validated_data)
        priestss=validated_data.pop('available_priests_ids',[])
        ceremony_obj=ceremony.objects.create(**validated_data)
        print(ceremony_obj)
        print(priestss)
        for i in priestss:
            print(i)
            #p=ceremony.objects.get(id=i)
            ceremony_obj.available_priests.add(i)
            print("that worked")
            ceremony_obj.save()
        #ed_data.pop('priests_ids')
        print(ceremony_obj.available_priests)
        return ceremony_obj

class location_serializer(serializers.ModelSerializer):
    class Meta:
        model= location
        fields='__all__'

class travel_serializer(serializers.ModelSerializer):
    locations_covered=location_serializer(read_only=True,many=True)
    location_ids=serializers.PrimaryKeyRelatedField(write_only=True,many=True,queryset=location.objects.all())
    class Meta:
        model=travel
        fields='__all__'

    def create(self,validated_data):
        locations=validated_data.pop('location_ids',[])
        travel_obj=travel.objects.create(**validated_data)
        for i in locations:
            travel_obj.locations_covered.add(i)
            travel_obj.save()
        return travel_obj

class products_cart_serializer(serializers.ModelSerializer):
    product=pooja_serializer(read_only=True)
    product_ids=serializers.PrimaryKeyRelatedField(write_only=True,queryset=color_quantity.objects.all())
    customer=app_users_serializer(read_only=True)
    customer_ids=serializers.PrimaryKeyRelatedField(write_only=True,queryset=app_users.objects.all())
    class Meta:
        model=product_cart
        fields='__all__'
    def create(self,validated_data):
        product=validated_data.pop('product_ids')
        customer=validated_data.pop('customer_ids')
        cart_obj=product_cart.objects.create(**validated_data,product=product,customer=customer)
        #cart_obj.product=product
        #cart_obj.customer=customer
        return cart_obj
    

class gift_request_serializer(serializers.ModelSerializer):
    product_associated=pooja_serializer(read_only=True)
    product_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=color_quantity.objects.all())
    raised_by=app_users_serializer(read_only=True)
    customer_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=app_users.objects.all())
    class Meta:
        model=gift_requests
        fields='__all__'
    def create(self,validated_data):
        product=validated_data.pop('product_id')
        customer=validated_data.pop('customer_id')
        request_obj=gift_requests.objects.create(**validated_data,product_associated=product,raised_by=customer)
        #cart_obj.product=product
        #cart_obj.customer=customer
        return request_obj

class ceremony_booking_serializer(serializers.ModelSerializer):
    ceremony_booked=ceremony_serializer(read_only=True)
    ceremony_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=ceremony.objects.all())
    priest_selected=priest_serializer(read_only=True)
    priest_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=priests.objects.all())
    user_associated=app_users_serializer(read_only=True)
    user_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=app_users.objects.all())
    class Meta:
        model=ceremony_bookings
        fields='__all__'
    def create(self,validated_data):
        ceremonyy=validated_data.pop('ceremony_id')
        priest=validated_data.pop('priest_id')
        customer=validated_data.pop('user_id')
        booking_obj=ceremony_bookings.objects.create(**validated_data,ceremony_booked=ceremonyy,priest_selected=priest,user_associated=customer)
        #cart_obj.product=product
        #cart_obj.customer=customer
        return booking_obj

class yatra_booking_serializer(serializers.ModelSerializer):
    yatra=travel_serializer(read_only=True)
    yatra_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=travel.objects.all())
    yatra_user=app_users_serializer(read_only=True)
    yatra_user_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=app_users.objects.all())
    class Meta:
        model=yatra_bookings
        fields='__all__'

    def create(self,validated_data):
        yatra=validated_data.pop('yatra_id')
        customer=validated_data.pop('yatra_user_id')
        booking=yatra_bookings.objects.create(**validated_data,yatra=yatra,yatra_user=customer)
        return booking    

