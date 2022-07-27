import email
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, ("Successfully logged in!!"))
            #redirect to the home page
        else:
            messages.success(request, ("There was an error logging in, Try again!!"))
            #redirect to the login page

    else:
        #redirect to the user login page
        pass

def logout_user(request):
    logout(request)
    messages.success(request, ("Successfully logged out!!"))
    #redirect to the home page

def register_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email = email):
                messages.error(request, 'Email already exists!')
                #redirect to the register user page
            else:
                user = User.objects.create_user(email=email, password=password)
                login(request, user)
                messages.success(request, 'You are now logged in.')
                user.save()
                messages.success(request, 'You are registered succesfully.')
                return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            #redirect to the register user page

    else:
        #redirect to the register user page
        pass

