from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from config import GOOGLE_MAPS_API_KEY
from models import *
import search


def index(request):
    restaurant_list = Restaurant.objects.all()
    context = {
        'api_key': GOOGLE_MAPS_API_KEY,
        'restaurant_list': restaurant_list
    }
    return render(request, 'dimsum/index.html', context)


def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect('index')


def signout(request):
    logout(request)
    return redirect('index')


def signup(request):
    return render(request, 'dimsum/signup.html')


def register(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password_confirmation = request.POST['password_confirmation']
    if password == password_confirmation:
        user = User.objects.create_user(
            username, email, password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('signup')
    else:
        return redirect('signup')


@login_required(login_url='index')
def settings(request):
    if request.user.is_authenticated:
        return render(request, 'dimsum/settings.html')
    else:
        return redirect('index')


def change_password(request):
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    new_password_confirmation = request.POST['new_password_confirmation']
    user = authenticate(username=request.user.username, password=old_password)
    if user is not None and new_password == new_password_confirmation:
        user.set_password(new_password)
        user.save()
        user = authenticate(username=request.user.username,
                            password=new_password)
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'dimsum/settings.html')


def searchResults(request):
    dish = request.POST['dish']
    results = search.search_dishes(dish)
    dishes = [result.name for result in results]
    context = {
        'dishes': dishes
    }
    return render(request, 'dimsum/results.html', context)
