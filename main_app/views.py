#from turtle import color
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from customers.models import gift_requests
from .models import permanent_Address,app_users,saved_Address,pooja_products,color_quantity,priests,ceremony,travel,location
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from rest_framework.views import APIView
# Create your views here.
import math, random
from django.contrib.auth.decorators import login_required
 
# function to generate OTP
@login_required(login_url='/login')
def generateOTP() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")

@login_required(login_url='/login')
def show_admin(request):
    if request.method=='POST':
        username=request.user.username
        print(request.user)
        user=app_users.objects.filter(email=username).first()
        user.name=request.POST["name"]
        user.email=request.POST["email"]
        user.phone=request.POST["phone"]
        user.save()
        return HttpResponseRedirect("/adminn/manage")
    username=request.user.username
    print(request.user)
    users=app_users.objects.filter(email=username).first()
    if(request.user.is_superuser or users.user_type=='Admin'):
        return render(request,'admin/view_profile.html',{'user':users})
    else:
        return HttpResponse("loggedin user is not admin")

def view_gift_requests(request):
    requests=gift_requests.objects.all()
    return render(request,'admin/view_gift_requests.html',{'requests':requests})

def accept_gift_request(request,pid):
    requests=gift_requests.objects.get(id=int(pid))
    requests.status="Accepted"
    requests.save()
    return HttpResponseRedirect('/adminn/view_gift_requests')
def reject_gift_request(request,pid):
    requests=gift_requests.objects.get(id=int(pid))
    requests.status="Rejected"
    requests.save()
    return HttpResponseRedirect('/adminn/view_gift_requests')
def add_location_admin(request):
    if request.method=='POST':
        location_obj=location()
        location_obj.city=request.POST["city"]
        location_obj.pin_code=request.POST["pincode"]
        location_obj.save()
        return HttpResponseRedirect("/adminn/view_yatras")
    return render(request,'admin/add_location.html')

def view_yatra_Admin(request):
    yatras=travel.objects.all()
    return render(request,'admin/view_yatras.html',{'yatras':yatras})

def delete_yatra_admin(request,pid):
    yatra=travel.objects.get(id=pid)
    yatra.delete()
    return HttpResponseRedirect('/adminn/view_yatras')

def edit_yatra_admin(request,pid):
    if request.method=='POST':
        
        yatra=travel.objects.get(id=int(pid))
        print(yatra.start_date)
        yatra.name=request.POST["name"]
        yatra.description=request.POST["description"]
        yatra.price=request.POST["price"]
        if request.POST["start"]:
            yatra.start_date=request.POST["start"]
        if request.POST["end"]:
            yatra.end_date=request.POST["end"]
        #yatra.end_date=request.POST["end"]
        if request.FILES:
            yatra.photo=request.FILES['photo']
        locations=request.POST.getlist("locations")
        
        yatra.save()
        yatra.locations_covered.clear()
        for i in locations:
            yatra.locations_covered.add(location.objects.get(id=int(i)))
        yatra.save()
        return HttpResponseRedirect('/adminn/view_yatras')
    yatra=travel.objects.get(id=int(pid))
    all_locations=location.objects.all()
    yatra_locations=yatra.locations_covered.all()
    other_locations=[]
    for locat in all_locations:
        if locat not in yatra_locations:
            other_locations.append(locat)
    return render(request,'admin/edit_yatra.html',{'yatra':yatra,'other_locations':other_locations})


def add_yatra_admin(request):
    if request.method=='POST':
        yatra=travel()
        yatra.name=request.POST["name"]
        yatra.description=request.POST["description"]
        yatra.price=request.POST["price"]
        yatra.start_date=request.POST["start"]
        yatra.end_date=request.POST["end"]
        if request.FILES:
            yatra.photo=request.FILES['photo']
        locations=request.POST.getlist("locations")
        yatra.save()
        for i in locations:
            yatra.locations_covered.add(location.objects.get(id=int(i)))
        yatra.save()
        return HttpResponseRedirect('/adminn/view_yatras')
    locations=location.objects.all()
    return render(request,'admin/add_yatra.html',{'locations':locations})
# for admins to add product
@login_required(login_url='/login')
def add_product(request):
    if request.method=='POST':
        name=request.POST["name"]
        size=request.POST["size"]
        description=request.POST["description"]
        photo=request.FILES['photo']
        price=request.POST["price"]
        color=request.POST["colour"].capitalize()
        quantity=request.POST["quantity"]
        search_prod=pooja_products.objects.filter(name=name,size=size)
        if search_prod.first():
            search_col_quant=color_quantity.objects.filter(color=color,quantity=quantity,product=search_prod.first())
            if search_col_quant.first():
                search_col_quant=search_col_quant.first()
                search_col_quant.quantity+=quantity
                search_col_quant.save()
            else:
                new_col_quant=color_quantity(color=color,quantity=quantity,price=price,product=search_prod.first(),photo=photo)
                new_col_quant.save()
        else:
            new_product=pooja_products(name=name,description=description,size=size)
            new_product.save()
            new_col_quant=color_quantity(color=color,price=price,quantity=quantity,product=new_product,photo=photo)
            new_col_quant.save()

        
    return render(request,'admin/add_products.html')
# for admins to add gifts
def add_gifts(request):
    if request.method=='POST':
        name=request.POST["name"]
        size=request.POST["size"]
        description=request.POST["description"]
        photo=request.FILES['photo']
        price=0
        color=request.POST["colour"].capitalize()
        quantity=request.POST["quantity"]
        search_prod=pooja_products.objects.filter(name=name,size=size)
        if search_prod.first():
            search_col_quant=color_quantity.objects.filter(color=color,quantity=quantity,product=search_prod.first())
            if search_col_quant.first():
                search_col_quant=search_col_quant.first()
                search_col_quant.quantity+=quantity
                search_col_quant.save()
            else:
                new_col_quant=color_quantity(color=color,quantity=quantity,price=price,product=search_prod.first(),photo=photo)
                new_col_quant.save()
        else:
            new_product=pooja_products(name=name,description=description,size=size)
            new_product.save()
            new_col_quant=color_quantity(color=color,price=price,quantity=quantity,product=new_product,photo=photo)
            new_col_quant.save()

        
    return render(request,'admin/add_gifts.html')

#for admins to view ceremonies
def view_ceremonies_admin(request):
    ceremonies=ceremony.objects.all()
    return render(request,'admin/view_ceremonies.html',{'ceremonys':ceremonies}) 
# for admins to edit ceremony
def edit_ceremony_admin(request,pid):
    if request.method=='POST':
        selected_priests=request.POST.getlist("priest")
        change_ceremony=ceremony.objects.get(id=pid)
        change_ceremony.name=request.POST['name']
        change_ceremony.price=request.POST['price']
        change_ceremony.description=request.POST['description']
        change_ceremony.available_priests.clear()
        if(request.FILES):
            change_ceremony.photo=request.FILES['photo']
        for priest in selected_priests:
            priest_obj=priests.objects.get(id=int(priest))
            change_ceremony.available_priests.add(priest_obj)
        change_ceremony.save()
        return HttpResponseRedirect('/adminn/view_ceremonies')


    current_ceremony=ceremony.objects.get(id=int(pid))
    ceremony_priests=current_ceremony.available_priests.all()
    all_priests=priests.objects.all()
    other_priests=[]
    for i in all_priests:
        if i not in ceremony_priests:
            other_priests.append(i)
    data={'ceremony':current_ceremony, 'other_priests':other_priests}
    return render(request,'admin/edit_ceremony.html',data)

def delete_ceremony_admin(request,pid):
    prod=ceremony.objects.get(id=int(pid))
    prod.delete()
    return(HttpResponseRedirect('/adminn/view_ceremonies'))
 # for admins to view product
def view_product_admin(request):
    products=color_quantity.objects.all()
    return render(request,'admin/view_products.html',{'products':products}) 

def delete_product_admin(request,pid):
    prod=color_quantity.objects.get(id=int(pid))
    pooja_prod=prod.product
    s=color_quantity.objects.filter(product=pooja_prod)
    if(len(s)==1):
        prod.delete()
        pooja_prod.delete()
    else:
        prod.delete()
    return(HttpResponseRedirect('/adminn/view_products'))
# for admins to edit product
def edit_product_admin(request,slug):  
    if request.method=='POST':
        prod=color_quantity.objects.get(slug=slug)
        prod.color=request.POST["colour"]
        prod.quantity=request.POST["quantity"]
        prod.product.name=request.POST["name"]
        prod.product.size=request.POST["size"]
        prod.price=request.POST["price"]
        prod.product.description=request.POST["description"]
        
        if(request.FILES):
            prod.photo=request.FILES['photo']
        prod.product.save()
        prod.save()
        return(HttpResponseRedirect('/adminn/view_products'))
    else:

        data=color_quantity.objects.get(slug=slug)
        return render(request,'admin/edit_product.html',{'prod':data})
# for admins to add ceremony
def add_ceremony(request):
    if request.method=='POST':
        priest_lists=request.POST.getlist('priest')
        new_ceremony=ceremony()
        new_ceremony.name=request.POST["name"]
        new_ceremony.price=request.POST["price"]
        new_ceremony.description=request.POST["description"]
        if request.FILES:

            new_ceremony.photo=request.FILES['photo']
        priest=int(request.POST["priest"])
        new_ceremony.save()
        for priest in priest_lists:
            priest_obj=priests.objects.get(id=int(priest))
            new_ceremony.available_priests.add(priest_obj)

        #new_ceremony.=priests.objects.get(id=priest)
        new_ceremony.save()
        return HttpResponseRedirect('/adminn/add_ceremony')
    priests_available=priests.objects.all()
    return render(request,'admin/add_ceremony.html',{'priests':priests_available})

def add_priest(request):
    if request.method=='POST':
        new_priest=priests()
        new_priest.name=request.POST["name"]
        new_priest.age=request.POST["age"]
        new_priest.contact_number=request.POST["phone"]
        new_priest.address=request.POST["address"]
        new_priest.save()
        return HttpResponseRedirect('/adminn/add_ceremony')
        

    return render(request,'admin/add_priest.html')
def register(request):
    print(request.method)
    if request.method=='POST':
        print("yes")
        print(request.POST["name"])
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        password=request.POST["pwd"]
        
        a=User(username=email)
        a.set_password(password)
        a.save()
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request, user)
            otp=generateOTP()
            msg="HI There , the otp to verify your account is :- " + str(otp)
            send_mail("Verify your Account",msg,'djangodemo72@gmail.com',[email])
            u=app_users(name=name,phone=phone,password=password,email=email,active=False,last_otp=otp)
            u.user_id=a
            u.save()
            return HttpResponseRedirect('/verifyOTP')
            #send mail
            #then send verify_otp page

    
    return render(request,'signup.html')



def userlogin(request):
    #print(request.user.username)
    
    if request.method=='POST':
        # msg="Hi"
        print(request.POST)
        email=request.POST["email"]
        #print(email)
        password=request.POST["pwd"]
        u=app_users.objects.filter(email=email,password=password).first()
        a=User.objects.filter(username=email).first()
        #print(a)
        user=authenticate(request,username=email,password=password)
        #print(a.is_superuser)
        if user:
            login(request, user)
            if a.is_superuser:
                return HttpResponseRedirect('/superadmin/manage')
            elif u.active:
                if u.user_type=='Admin':
                    return HttpResponseRedirect('/adminn/manage')
                            
                else:
                            #link for landing page
                    return HttpResponseRedirect('/customer/home')
                            #redirect to customer page
                    
            else:
                if u.user_type=='Admin':
                    return HttpResponse('inactive admin')
                else:
                    digits = "0123456789"
                    OTP = ""
 
                    for i in range(4) :
                        OTP += digits[math.floor(random.random() * 10)]
                    u.last_otp=OTP
                    u.save()
                    msg="HI There , the otp to verify your account is :- " + str(OTP)
                    send_mail("Verify your Account",msg,'djangodemo72@gmail.com',[email])
                    return HttpResponseRedirect('/verifyOTP')

        else:
            return HttpResponse('invalid credentials')

    return render(request,'login.html')
@login_required(login_url='login')    
def verify_otp(request):
    if request.method=='POST':
        username=request.user.username
        user=app_users.objects.filter(email=username).first()
        given_otp=int(request.POST["otp"])
        print(type(user.last_otp))
        print(type(given_otp))
        if user.last_otp==given_otp:
            user.active=True
            user.save()
            return HttpResponseRedirect('/adduserdetails')
        else:
            return(HttpResponse("incorrect OTP"))
    return render(request,'verifyOTP.html')
@login_required(login_url='login')
def resend_otp(request):
    username=request.user.username
    user=app_users.objects.filter(email=username).first()
    otp=generateOTP()
    user.last_otp=otp
    user.save()
    msg="HI There , the otp to verify your account is :- " + str(otp)
    send_mail("Verify your Account",msg,'djangodemo72@gmail.com',[username])
    return HttpResponseRedirect('/verifyOTP')

@login_required(login_url='login')
def add_user_details(request):
    if request.method=='POST':
        username= request.user.username
        user= app_users.objects.filter(email=username).first()
        user.phone= request.POST["phone"]
        user.alternate_phone= request.POST["alternatephone"]
        user.anniversary=request.POST["anniversary"]
        user.date_of_birth=request.POST["dob"]
        user.save()

        perm_address=permanent_Address()
        perm_address.address=request.POST["perm_address"]
        perm_address.landmark=request.POST["perm_landmark"]
        perm_address.pincode=request.POST["perm_pincode"]
        perm_address.city=request.POST["perm_City"]
        perm_address.state=request.POST["perm_State"]
        perm_address.country=request.POST["perm_Country"]
        perm_address.save()
        user.permanent_Address=perm_address
        user.save()

        delivery_address= saved_Address()
        delivery_address.address=request.POST["delivery_address"]
        delivery_address.landmark=request.POST["delivery_landmark"]
        delivery_address.pincode=request.POST["delivery_pincode"]
        delivery_address.city=request.POST["delivery_City"]
        delivery_address.state=request.POST["delivery_State"]
        delivery_address.country=request.POST["delivery_Country"]
        delivery_address.user=user
        delivery_address.save()
        
        #link for landing page
        return HttpResponseRedirect('/landingpage')

    return render(request,'add_details.html')

@login_required(login_url='login')
def landingpage(request):
    return render(request,'landing_page.html')