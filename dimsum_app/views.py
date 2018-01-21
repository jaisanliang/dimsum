from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
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
    #results = search.search_dishes(dish)
    results = Dish.objects.filter(name__contains=dish).order_by('-rating')
    # dishes = [(result.name, result.restaurant_id, result.restaurant_name)
    #          for result in results]
    dishes = [(result, result.restaurant.id, result.restaurant.name)
              for result in results]
    context = {
        'dishes': dishes
    }
    return render(request, 'dimsum/results.html', context)


def restaurant(request):
    restaurant_id = request.GET['id']
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    dishes = Dish.objects.filter(restaurant=restaurant)
    context = {
        'restaurant': restaurant,
        'dishes': dishes
    }
    return render(request, 'dimsum/restaurant.html', context)


def dish(request):
    food_id = request.GET['id']
    restaurant_id, dish = food_id.split('_')
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    dish = Dish.objects.filter(restaurant_id=restaurant_id, name=dish)[0]
    reviews = Review.objects.filter(dish=dish)
    context = {
        'restaurant': restaurant,
        'dish': dish,
        'reviews': reviews
    }
    return render(request, 'dimsum/dish.html', context)


def write_review(request):
    restaurant_id = request.POST['restaurant_id']
    dish_name = request.POST['dish_name']
    review_text = request.POST['review']
    rating = int(request.POST['rating'])
    dish = Dish.objects.filter(restaurant_id=restaurant_id, name=dish_name)[0]
    dish.rating = 1.0 * (float(dish.rating) *
                         dish.num_ratings + rating) / (dish.num_ratings + 1)
    dish.num_ratings += 1
    dish.save()
    review = Review.objects.create(
        dish=dish, review=review_text, rating=rating, author=request.user)
    return HttpResponseRedirect('dish?id={}_{}'.format(restaurant_id, dish_name))


def delete_review(request):
    restaurant_id = request.POST['restaurant_id']
    dish_name = request.POST['dish_name']
    review_id = request.POST['id']
    review = Review.objects.get(id=review_id)
    dish = Dish.objects.filter(restaurant_id=restaurant_id, name=dish_name)[0]
    if dish.num_ratings == 1:
        dish.rating = 0
    else:
        dish.rating = 1.0 * (float(dish.rating) *
                             dish.num_ratings - review.rating) / (dish.num_ratings - 1)
    dish.num_ratings -= 1
    dish.save()
    review.delete()
    return HttpResponseRedirect('dish?id={}_{}'.format(restaurant_id, dish_name))
