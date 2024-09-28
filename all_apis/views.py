
from django.shortcuts import get_object_or_404
from .serializers import otp_serializer, app_users_serializer, login_serializer, product_serializer,ceremony_serializer,pooja_serializer,seperate_pd_serializer,location_serializer,travel_serializer,products_cart_serializer,ceremony_booking_serializer,yatra_booking_serializer,gift_request_serializer
from main_app.models import app_users,pooja_products,color_quantity,ceremony,priests,location,travel
from customers.models import ceremony_bookings,product_cart,gift_requests,yatra_bookings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
import json
import math,random
import base64
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework import generics,mixins,viewsets,status,permissions,filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

#-*-*-*-*-*-*-*-*-*-*-admin based operations-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        return img
    except:
        return None

def temp_view(request):
    return(0)


'''class apilogin(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=login_serializer
    authentication_classes=[]
    permission_classes=[]
    def create(self,request):
        #queryset=User.objects.all()
        print(request.data)
        user = get_object_or_404(User, username=request.data['username'])
        serializer=login_serializer(user)
        return Response(serializer.data)'''
    
class apilogin(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=login_serializer
    authentication_classes=[]
    permission_classes=[]
    def post(self,request):
        #queryset=User.objects.all()
        print(request)
        print(request.data)
        user=authenticate(request,username=request.data['username'],password=request.data['password'])
        
        if(user):
            login(request,user)
            app_user_obj=get_object_or_404(app_users, email=request.data['username'])
            serializer=app_users_serializer(app_user_obj)
            return Response(serializer.data)
        else:
            response = {
           "message": "invalid credentials",
           
           }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
            

class apiRegister(generics.CreateAPIView,generics.RetrieveUpdateAPIView):
    queryset=app_users.objects.all()
    serializer_class=app_users_serializer
    authentication_classes=[]
    permission_classes=[]
    def post(self,request):
        return self.create(request)
    def put(self,request,pk):
        
        print(self)
        return self.update(request,pk)
    
    #def get(self,request,pk):
    #    return self.retrieve(request,pk)   
#@api_view(['post'])
@permission_classes((permissions.AllowAny,))
class verify_otp(APIView):
    def post(self,request):
        if(request.user.is_anonymous):
            print(request.user)
            return Response({'detail':'authentication not provided'})
        serializer=otp_serializer(data=request.data)
        if serializer.is_valid():
            user_obj=app_users.objects.filter(user_id=request.user).first()
            #print(user_obj.last_otp)
            if(user_obj.last_otp == int(request.data['otp'])):
                user_obj.active=True
                user_obj.save()
                return Response({'otp_valid':True})
            else:
                return Response({'otp_valid':False})
        else:
            return Response({'errors':serializer.errors})

@permission_classes((permissions.AllowAny,))
class forgot_pwd(APIView):
    def post(self,request):
        #write code here to check if email is valid or not later
        user_obj=app_users.objects.filter(email=request.data['email']).first()
        if(user_obj):
            digits = "0123456789"
            OTP = ""
            for i in range(4) :
                OTP += digits[math.floor(random.random() * 10)]
            msg="HI There , the otp to verify your account is :- " + str(OTP)
            send_mail("Verify your Account",msg,'djangodemo72@gmail.com',[request.data['email']])
            user_obj.last_otp=OTP
            user_obj.save()
            return Response({'detail':"otp sent"},status=status.HTTP_200_OK)
        else:
            return Response({'detail':"user does not exist"},status=status.HTTP_404_NOT_FOUND)


class Color_quant_list(viewsets.ModelViewSet):
    queryset=color_quantity.objects.all()
    serializer_class=pooja_serializer
    authentication_classes=[]
    permission_classes=[]
    filter_backends=[filters.SearchFilter]
    search_fields = ['product__name','color']
class Prdo_list(viewsets.ModelViewSet):
    queryset=pooja_products.objects.all()
    serializer_class=seperate_pd_serializer
    
class Products_list(viewsets.ModelViewSet):
    queryset=pooja_products.objects.all()
    serializer_class=product_serializer
    parser_classes=(JSONParser,MultiPartParser,FormParser)
    
    

class Ceremony_operations(viewsets.ModelViewSet):
    queryset=ceremony.objects.all()
    serializer_class=ceremony_serializer
    authentication_classes=[]
    permission_classes=[]
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['available_priests']
    
class Location_lists(viewsets.ModelViewSet):
    queryset=location.objects.all()
    serializer_class=location_serializer
    

class Travel_lists(viewsets.ModelViewSet):
    queryset=travel.objects.all()
    serializer_class=travel_serializer
    
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*    


# -*-*-*-*-*-*-*-*-*-customer based operations-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class Products_cart_lists(viewsets.ModelViewSet):
    queryset=product_cart.objects.all()
    serializer_class=products_cart_serializer
    
    

class Ceremony_bookings_lists(viewsets.ModelViewSet):
    queryset=ceremony_bookings.objects.all()
    serializer_class=ceremony_booking_serializer
    
class Yatra_bookings(viewsets.ModelViewSet):
    queryset=yatra_bookings.objects.all()
    serializer_class=yatra_booking_serializer
    http_method_names=['get','post','put','delete']
    
'''class yatra_bookings_lists(generics.ListCreateAPIView):
    queryset=yatra_bookings.objects.all()
    serializer_class=yatra_booking_serializer'''
    
    
'''class gift_request_lists(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=gift_requests.objects.all()
    serializer_class=gift_request_serializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)'''
    
class Gift_request_lists(viewsets.ModelViewSet):
    queryset=gift_requests.objects.all()
    serializer_class=gift_request_serializer
    
