from django.shortcuts import render,redirect
from django.contrib.auth.models import  User,auth
from django.contrib import messages
from product.views import Customer

def login(request):
    if request.method=="POST":
        userid=request.POST['userid']
        password=request.POST['password']
        user = auth.authenticate(username=userid,password=password)
        if user!=None:
            auth.login(request,user)  
            print('logged in')
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('signin')
    else:
        return render(request,'customer/signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')


def register(request):

    if request.method=="POST":
        
        userid=request.POST['userid']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        pass1=request.POST['password']
        pass2=request.POST['conf-password']
        
        if(pass1==pass2):
            if User.objects.filter(username=userid).exists():
                print('user id exists')
                messages.info(request,'User id exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=userid,first_name=firstname,last_name=lastname,password=pass1)
                user.save()
                customer=Customer(user=user,name=firstname+" "+lastname,email="",address="")
                customer.save()
                return redirect('signin')
        else:
            messages.info(request,'password does not match!')
            return redirect('signup')

        return redirect('signin')

    return render(request,'customer/signup.html')

