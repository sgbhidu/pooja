from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from main_app.models import app_users
# Create your views here.
def manage_Admin(request):
    if(request.user.is_superuser):
        admins=app_users.objects.filter(user_type='Admin')

        return render(request,'superadmin/manage_admins.html',{'users':admins})
    else:
        return HttpResponseRedirect('/login')
def create_Admin(request):
    if request.method=='POST':
        print("yes")
        print(request.POST["name"])
        name=request.POST["name"]
        email=request.POST["email"]
        password=request.POST["pwd"]
        u=app_users(name=name,email=email,password=password,user_type='Admin',active=True)
        
        a=User(username=email)
        a.set_password(password)
        a.save()
        u.user_id=a
        u.save()

    return render(request,'superadmin/create_admin.html')

def change_admin_status(request,id):
    print(request.method)
        #id=request.POST["admin_id"]
    user=app_users.objects.get(id=id)
    if user.active:
        user.active=False
    else:
        user.active=True
    user.save()
    return HttpResponseRedirect('/superadmin/manage')
