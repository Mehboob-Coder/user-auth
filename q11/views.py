
###2
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from .helpers import send_forget_password_mail
import uuid

# Login view
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both Username and Password are required')
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login/')
        
        login(request, user)
        return redirect('/')

    return render(request, 'login.html')

# Register view
def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken.')
            return redirect('/register/')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken.')
            return redirect('/register/')

        user_obj = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user_obj)

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('/login/')

    return render(request, 'register.html')

# Logout view
def Logout(request):
    logout(request)
    return redirect('/')

# Home view
@login_required(login_url='/login/')
def Home(request):
    return render(request, 'home.html')

# Change password view
def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.get(forget_password_token=token)
        user = profile_obj.user

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect(f'/change_password/{token}/')

            user.set_password(new_password)
            user.save()

            # profile_obj.forget_password_token = token
            # profile_obj.save()

            messages.success(request, 'Password changed successfully. Please log in.')
            return redirect('/login/')

        context = {'token': token}
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid or expired token.')
        return redirect('/forget_password/')

    return render(request, 'change-password.html', context)

# Forget password view
def ForgetPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'No user found with this username.')
            return redirect('/forget_password/')

        user_obj = User.objects.get(username=username)
        token = str(uuid.uuid4())
        profile_obj = Profile.objects.get(user=user_obj)
        profile_obj.forget_password_token = token
        profile_obj.save()

        send_forget_password_mail(profile_obj.user.email, token)

        messages.success(request, 'An email has been sent with instructions to reset your password.')
        return redirect('/forget_password/')

    return render(request, 'forget_password.html')


