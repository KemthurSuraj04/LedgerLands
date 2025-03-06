
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from . models import *

from django.contrib.auth import logout

from . import helper

from web3 import Web3


def landing(request):
    return render(request,'landing.html')

def registration(request):
    if request.method == "POST":
        account_address = request.POST.get("account-address")
        name = request.POST.get('name')
        email=request.POST.get('email')
        age = int(request.POST.get('age'))
        city=request.POST.get('city')
        aadhar_number = request.POST.get('aadhar_number')
        pan_number = request.POST.get('pan_number')
        pwd=request.POST.get('password')
        #aadhar_doc = request.FILES.get('aadhar_doc')
    
        
            #city = request.POST.get("city")
        user = User(
            address=account_address,
            name=name,
            age=age,
            city=city,
            aadhar_number=aadhar_number,
            pan_number=pan_number,
            document="lets say some document url",
            email=email,
            password=pwd
        )
            
        Details={
            "id":account_address,
            "name":name,
            "age":age,
            "city":city,
            "aadharNumber":aadhar_number,
            "panNumber":pan_number,
            "document":"lets say some hash of the document",
            "email":email,
            "pwd":pwd
                
        }
            
        status=helper.registerUser(Details)  #written logic elsewhere
            
        user.save()
            
        
        if status==1:
            return HttpResponse("SUCCESS")
        
        else:
            return HttpResponse("FAILED")
        
        
    
    return render(request,'registration.html')

# Create your views here.


def login(request):
    if request.method == 'POST':
       
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email=="registrar@gmail.com":
            return HttpResponse("You are not allowed to login")
        
        else:
            try:
                user = User.objects.get(email=email)
            except:
                return HttpResponse("USER EMAIL DOESNT EXIST")
            if password==user.password:
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                return HttpResponse("Invalid Password")

        
        #elif Admin.objects.filter(email=email, password=password).exists():
        #    user = Admin.objects.get(email=email)
        #    request.session['user_id'] = user.id
        #    request.session['role'] = 'admin'
        #    return redirect('dashboard')

        #else:
            #return render(request, 'login.html', {'error': 'Invalid Email-ID or Password, Please Try Again...'})
                
    return render(request,'login.html')


def dashboard(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user=User.objects.get(id=user_id)

    
    
        return render(request, 'dashboard.html', {'user': user})
    else:
        return HttpResponse("PLEASE LOGIN")
    '''elif role == 'seller':
        #user = Seller.objects.get(id=user_id)
        print('hi')
    #elif role == 'admin':
    #    user = Admin.objects.get(id=user_id)
    else:
        return redirect('login')  # Unknown role, redirect to login'''
        
        
        
        
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.get(email=email)
        request.session['user_id'] = user.id
        return redirect('admin_dashboard')
    return render(request,'admin-login.html')
    
    
    
def admin_dashboard(request):
    return render(request,'admin-dashboard.html',{'registered':1,'verified':1,'Vlands':100})




def logout1(request):
    logout(request)
    
    return redirect('landing')



def unverifiedusers(request):
    users = User.objects.exclude(email='registrar@gmail.com')
    return render(request,'unverifiedusers.html',{'users':users})


def unverifiedlands(request):
    lands=Landreg.objects.all()
    return render(request,'unverifiedlands.html',{'lands':lands})


def unverifyuser(request):
    return render(request,'unverifyuser.html')
    
    
def unverifyland(request):
    return render(request,'unverifyland.html')


def registerland(request):
    if request.method=='POST':
        area=request.POST.get('area')
        city=request.POST.get('city')
        state=request.POST.get('state')
        landPrice=request.POST.get('landPrice')
        propertyId=request.POST.get('propertyPID')
        physicalSurveyNumber=request.POST.get('physicalSurveyNumber')
        ipfsHash=request.POST.get('ipfsHash')
        document=request.POST.get('document')
        
        jsonObject={'area':area,
                    'city':city,
                    'state':state,
                    'landPrice':landPrice,
                    'propertyPID':propertyId,
                    'physicalSurveyNumber':physicalSurveyNumber,
                    'ipfsHash':ipfsHash,
                    'document':document}
        
        return JsonResponse(jsonObject)
    
    
        
    return render(request,'registerland.html')



def user_details(request,id):
    
    user=User.objects.get(id=id)
    return render(request,'user_details.html',{'user':user})


def land_details(request,id):
    
    land=Landreg.objects.get(id=id)
    return render(request,'land_details.html',{'land':land})


