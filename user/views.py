from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
# Create your views here.
def Login(request):
      if request.method == "POST":
             username= request.POST['username']
             password= request.POST['password']
             
             user= authenticate(username= username,password= password)
             if user is not None:
                    login(request,user)
                    messages.add_message(request,messages.SUCCESS,'Successfully Login ')
                    return redirect('library:dashboard')
      return render(request,'user/login.html')
def Logout(request):
   logout(request)
   messages.add_message(request,messages.SUCCESS,'Successfully Logout')
   return redirect('user:user_login')
# def Register_view(request):
#    if request.method == "POST":
#           forms = RegistrationForm(request.POST)
#           if forms.is_valid():
#                   forms.save()
#                   messages.SUCCESS(request,"successfully registered")
#                   return redirect("user:user_login")
#           else:
#                  print("form is invalid")
                   
#    else:
#        forms= RegistrationForm()
#    return render(request,'user/register.html',{"forms" : forms})      
def Register_view(request):
    if request.method == "POST":
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            # login(request,user)
            messages.success(request,"Registration successful")
            return redirect('user:user_login')
    else:
        
        forms=RegistrationForm()
    return render(request,"user/register.html",{"form":forms})           