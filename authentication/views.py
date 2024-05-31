from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import userdetails

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            userdetails.objects.create(user=user, phone_number=phone_number, email=email)
            # messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    return render(request, 'registration/register.html')
    #         if user is not None:
    #             login(request, user)
    #             return redirect('dashboard')
    #         else:
    #             messages.error(request, 'Registration successful but authentication failed. Please try logging in.')
    # return render(request, 'registration/register.html')
from django.contrib.auth import login as authlogin
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            authlogin(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('app/dashboard')
#         else:
#             return redirect('login')
#     return render(request,'registration/login.html')

# def dashboard(request):
#     return render(request,'registration/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

