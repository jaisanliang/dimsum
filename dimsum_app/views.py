from django.http import HttpResponse
from django.shortcuts import render

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


def signup(request):
    return render(request, 'dimsum/signup.html')


def register(request):
    username = request.POST['username']
    email = request.POST['email']
    user = User(username=username, email=email)
    user.save()
    context = {
        'user': user
    }
    return render(request, 'dimsum/registered.html', context)


def searchResults(request):
    dish = request.POST['dish']
    results = search.search_dishes(dish)
    dishes = [result.name for result in results]
    context = {
        'dishes': dishes
    }
    return render(request, 'dimsum/results.html', context)
