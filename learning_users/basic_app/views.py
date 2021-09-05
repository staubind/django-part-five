from django.contrib import auth
from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.models import User

# for user stuff
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    registered = False

    if request.method=='POST':
        print(request.POST)
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False) # save user to database (idk about commit=False, maybe it'll throw an error on line 19 now, because set_password is only for saved models or something)
            user.set_password(user.password) # hashes the password
            user.save() # save it to the db again..?
            # won't this save the password in plain text for some time before it hashes the password?
            # why not set_password to hash before saving it?
            profile = profile_form.save(commit=False)
            profile.user = user # connect the profile to the user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'basic_app/registration.html', context={"user_form":user_form,
                                                                    "profile_form":profile_form,
                                                                    "registered":registered})

@login_required
def special(request):
    return HttpResponse("You are logged in, nice!")

# @login_required makes sure the person must be logged in to hit this node.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        # get username and password
        username = request.POST.get('username') # get value from name="username" from the basic html form on the login.html page
        password = request.POST.get('password')
        # django's inbuilt authentication functions:
        user = authenticate(username=username, password=password)
        # authenticate returns a user object
        if user:
            # check that they're active - part of django's built-in user model
            if user.is_active:
                # log them in
                login(request, user)
                return HttpResponseRedirect(reverse('index')) # 
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print(f"Username: {username} and password {password}")
            return HttpResponse("invalid login details supplied")
    else:
        return render(request, 'basic_app/login.html',{})