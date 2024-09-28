#from turtle import color
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import gift_requests,product_cart,ceremony_bookings, yatra_bookings,prod_and_amount,product_orders
from main_app.models import permanent_Address,product_ratings,app_users,saved_Address,pooja_products,color_quantity,priests,ceremony,travel,location
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from customers import Checksum
# Create your views here.
from datetime import datetime
import math, random, stripe
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum
from django.db.models import Q


def homepage(request):
    return render(request,'customers/view_catalog.html')

def view_products(request):
    key=""
    selected_price=50
    colors=[]
    ticked_colours={}
    ticked_products={}
    product_names=[]
        
    products=color_quantity.objects.filter(price__gt=0)
    prods=[]
    for product in products:
        ticked_colours["product.color"]=False
        ticked_products["product.product.name"]=False
        colors.append(product.color)
        
        product_names.append(product.product.name)
    colors=list(set(colors))
    product_names=list(set(product_names))
    
    if request.method=='POST':
        print(request.POST)
        colours=request.POST.getlist("colour")
        if(colours):
            print("yes")
        prdcts=request.POST.getlist("product")
        print(colours)
#        all_objs=color_quantity.objects.all()
        if(colours):
            products=products.filter(color__in=colours)
        if(request.POST['range']):
            products=products.filter(price__lte=int(request.POST['range']))
            selected_price=int(request.POST['range'])
        if(prdcts):
            products=products.filter(product__name__in=prdcts)
        #a=color_quantity.objects.filter(color__in=colours,price__lte=request.POST['range'],product__name__in=prdcts)
        print(products)

    for product in products:
        a={}
        ratings=0
        rating_objs=product_ratings.objects.filter(product=product)
        if rating_objs:
            for objs in rating_objs:
                ratings+=objs.rating
        a['product']=product
        a['ratings']=ratings
        ticked_colours["product.color"]=True
        ticked_products["product.product.name"]=True
        prods.append(a)
        
    
    data={
        'products':prods,
        'key':key,
        'colors':colors,
        'ticked_colours':ticked_colours,
        'product_names':product_names,
        'ticked_products':ticked_products,
        'selected_price':selected_price
        }
        
    return render(request,'customers/view_products.html',data)
    #return render(request,'customers/pd_details.html',{'products':products,'key':key})

stripe.api_key='sk_test_51NSxDWSIdDYBrHxjt1phOqbOcuxu9jPd1fv8pGULuTMCxxXy517uqjmwLpMXxisYYEtr0wK30nFRIIBE6RfdNcIX00PE8P3qxj'
endpoint_secret = 'whsec_2d0804ff28435f041eb1ac8358ef0c0a05a24c85400e95b7f9950b31ccebbb99'
def view_products_cart(request):
    
    user=app_users.objects.filter(email=request.user.username).first()
    cart_objs=product_cart.objects.filter(customer=user)
    units=0
    for obj in cart_objs:
        units+=obj.quantity
    addresses=saved_Address.objects.filter(user=user)
    for address in addresses:
        if(address.default):
            default_address=address
    return render(request,'customers/view_cart.html',{'cart_objs':cart_objs,'units':units, 'addresses':addresses,'default_address':default_address})

def remove_cart_item(request,slug):
    user=app_users.objects.filter(email=request.user.username).first()
    prod=color_quantity.objects.get(slug=slug)
    cart_obj=product_cart.objects.filter(customer=user,product=prod)
    cart_obj.delete()
    return HttpResponseRedirect('/customer/view_products_cart')


def initiate_payment(request,order_type):
    if request.method=='POST':
        print(request.POST)
        all_products=request.POST.getlist('prod_id')
        print(all_products)
        all_prices=request.POST.getlist('prod_price')
        all_quantities=request.POST.getlist('prod_quantity')
        prod_order_obj=product_orders()
        a=product_orders.objects.all()
        order_id="ORD"
        if(len(a)>0):
            number=int(a[len(a)-1].order_id[3::])+1
            idd=str(number)
            
            order_id+="0"*(11-len(idd)) + str(number)
        else:
            order_id+="0"*11
        prod_order_obj.order_id=order_id
        prod_order_obj.date=datetime.now()
        prod_order_obj.amount=int(request.POST['total_amount'])
        user=app_users.objects.filter(email=request.user.username).first()
        prod_order_obj.done_by=user
        prod_order_obj.save()
        for i in range(0,len(all_products)):
            product=color_quantity.objects.get(id=int(all_products[i]))
            amount=float(all_prices[i])
            quantity=int(all_quantities[i])
            prodAmtObjs=prod_and_amount.objects.filter(product=product,price=amount,quantity=quantity)
            if (len(prodAmtObjs)==0):
                prod_amt_obj=prod_and_amount(product=product,price=amount,quantity=quantity)
                prod_amt_obj.save()
            else:
                prod_amt_obj=prodAmtObjs.first()
            prod_order_obj.products_associated.add(prod_amt_obj)

        '''CALLBACK_URL='https://securegw.paytm.in/theia/paytmCallback?ORDER_ID='+str(prod_order_obj.order_id)'''   
        '''param_dict = {

                'MID': 'BXgoSX63969954611254',
                'ORDER_ID': str(prod_order_obj.order_id),
                'TXN_AMOUNT': str(float(amount)),
                'CUST_ID': "sgbhidu288@gmail.com",
                #'CUST_ID': request.user.username,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':"http://127.0.0.1:8000/customer/handlerequest/"

        }'''
        '''param_dict={
            "merchantId": "MERCHANTUAT",
            "merchantTransactionId": "MT7850590068188104",
            "merchantUserId": "MUID123",
            "amount": 10000,
            "redirectUrl": "https://webhook.site/redirect-url",
            "redirectMode": "POST",
            "callbackUrl": "https://webhook.site/callback-url",
            "mobileNumber": "9999999999",
            "paymentInstrument": {
                "type": "PAY_PAGE"
             }
            }
        MERCHANT_KEY='B7Vd4Svc_pxE&moL'
        #chcksm=PaytmChecksum.generateSignature(param_dict, MERCHANT_KEY)
       # param_dict['CHECKSUMHASH'] = chcksm
        #print(PaytmChecksum.verifySignature(param_dict, "B7Vd4Svc_pxE&moL",param_dict['CHECKSUMHASH']))
        print(param_dict)
        print(prod_order_obj.order_id)
        return render(request, 'customers/paytm.html', {'param_dict': param_dict})'''
        success_url="http://127.0.0.1:8000/customer/payment_success/"+order_type+"/"+str(prod_order_obj.order_id)
        session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            
            'currency': 'inr',
            'product_data': {
                #'id':prod_order_obj.order_id,
            'name': 'T-shirt',
            },
            'unit_amount': str((prod_order_obj.amount)*100),
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url='http://localhost:4242/customer/payment_cancel',
        )
        print(session)
        return redirect(session.url, code=303)

def product_checkout(request):
    if request.method=='POST':
        print(request.POST)
        product=color_quantity.objects.get(id=int(request.POST['prod_id']))
        price=request.POST['prod_price']
        quantity=request.POST['quantity']
        total=int(price)*int(quantity)
        user=app_users.objects.filter(email=request.user.username).first()
        addresses=saved_Address.objects.filter(user=user)
        for address in addresses:
            if(address.default):
                default_address=address
        return render(request,'customers/product_checkout.html',{'product':product,'quantity':quantity,'price':price,'total':total ,'addresses':addresses,'default_address':default_address})
                                   
@csrf_exempt
def stripe_webhook(request):
    payload=request.body
    print(payload)
    print("\n request \n")
    for key,value in request.items():
        print(key)
    sig_header= request.META['HTTP_STRIPE_SIGNATURE']
    event=None
    try:
        event=stripe.Webhook.construct_event(payload,sig_header,endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event.type=='checkout.session.completed':
        session=event.data.object
        if session.mode=='payment' and session.payment_status=='paid':
            try:
                order=product_orders.objects.get(id=session.client_reference_id)
            except product_orders.DoesNotExist:
                return HttpResponse(status=404)
            order.payment_status="Success"
            order.save()
            
    return HttpResponse(status=200)

def view_order(request,order_id):
    user=app_users.objects.filter(email=request.user.username).first()
    cart_objs=product_cart.objects.filter(customer=user)
    if(len(cart_objs)>0):
        for obj in cart_objs:
            obj.delete()
    order=product_orders.objects.get(order_id=order_id)
    return render(request,'customers/order_details.html',{'order':order})

def payment_success(request,order_type,order_id):
    user=app_users.objects.filter(email=request.user.username).first()
    if(order_type=="cart_order"):
        cart_objs=product_cart.objects.filter(customer=user)
        if(len(cart_objs)>0):
            for obj in cart_objs:
                obj.delete()
    order=product_orders.objects.get(order_id=order_id)
    order.payment_status="Success"
    order.save()
    url='/customer/order_details/'+str(order_id)
    return HttpResponseRedirect(url)
    #return(HttpResponse("success"))
def payment_cancel(request):
    print(request)
    return(HttpResponse("cancel"))

def order_history(request):
    user_obj=app_users.objects.filter(email=request.user.username).first()
    if user_obj:
        orders=product_orders.objects.filter(done_by=user_obj)
        return render(request,'customers/order_history.html',{'orders':orders})
    return HttpResponseRedirect("login again")

@csrf_exempt
def handlerequest(request):
    print(request.POST)
    return render(request,'customers/handlerequest.html',{'param_dict': request.POST})
def view_gifts(request):
    products=color_quantity.objects.filter(price=0)
    return render(request,'customers/view_gifts.html',{'products':products})

def view_gift_details(request,slug):
    if request.method=='POST':
        gift=color_quantity.objects.get(slug=slug)
        user=app_users.objects.filter(email=request.user.username).first()
        cart_objs=product_cart.objects.filter(product=gift,customer=user).first()
        if(cart_objs):
            print(cart_objs.quantity)
            print(int(request.POST["quantity"]))
            cart_objs.quantity=cart_objs.quantity+int(request.POST["quantity"])
            #cart_objs.quantity=10
            cart_objs.save()
            print(cart_objs.quantity)
        elif(int(request.POST["quantity"])>0):
            prod_cart_obj=product_cart()
            prod_cart_obj.product=gift
            prod_cart_obj.quantity=int(request.POST["quantity"])
            prod_cart_obj.customer=user
            prod_cart_obj.payment_status="Waiting"
            prod_cart_obj.save()
    gifte=color_quantity.objects.get(slug=slug)
    prod_variants=color_quantity.objects.filter(product=gifte.product,price__gt=0)
    return render(request,'customers/product_details.html',{'gift':gifte,'variants':prod_variants})

def add_gift_request(request,pid):
    user=app_users.objects.filter(email=request.user.username).first()
    product=color_quantity.objects.get(id=int(pid))
    request_already_present=gift_requests.objects.filter(raised_by=user,product_associated=product).first()
    if not request_already_present:
        gifts=gift_requests(raised_by=user,product_associated=product)
        gifts.save()
    return HttpResponseRedirect('/customer/view_gift_requests')

def view_ceremonies(request):
    ceremonies=ceremony.objects.all()
    return render(request,'customers/view_ceremonies.html',{'ceremonys':ceremonies}) 

def schedule_ceremony(request,pid):
    if(request.method=='POST'):
        new_booking=ceremony_bookings()
        new_booking.ceremony_booked=ceremony.objects.get(id=int(pid))
        new_booking.user_associated=app_users.objects.filter(email=request.user.username).first()
        new_booking.priest_selected=priests.objects.get(id=int(request.POST["priest"]))
        new_booking.date_scheduled=request.POST["time"]
        new_booking.save()
        return HttpResponseRedirect('/customer/view_ceremonies')
        
        
    current_ceremony=ceremony.objects.get(id=int(pid))
    return render(request,"customers/schedule_ceremony.html",{'ceremony':current_ceremony})

def book_yatra(request,pid):
    if(request.method=='POST'):
        new_bookings=yatra_bookings()
        new_bookings.yatra=travel.objects.get(id=int(pid))
        new_bookings.yatra_user=app_users.objects.filter(email=request.user.username).first()
        new_bookings.save()
        return HttpResponseRedirect('/customer/view_yatras')
    current_yatra=travel.objects.get(id=int(pid))
    return render(request,"customers/book_yatra.html",{'yatra':current_yatra})



def view_gift_requests(request):
    current_user=app_users.objects.filter(email=request.user.username).first()
    user_requests=gift_requests.objects.filter(raised_by=current_user)
    return render(request,'customers/view_gift_requests.html',{'requests':user_requests})

def view_yatras(request):
    yatras=travel.objects.all()
    return render(request,'customers/view_yatras.html',{'yatras':yatras})

def view_ceremony_bookings(request):
    bookings=ceremony_bookings.objects.all()
    return render(request,'customers/view_ceremony_bookings.html',{'bookings':bookings})

def view_yatra_bookings(request):
    bookings=yatra_bookings.objects.filter(yatra_user=app_users.objects.filter(email=request.user.username).first())
    return render(request,'customers/view_yatra_bookings.html',{'bookings':bookings})