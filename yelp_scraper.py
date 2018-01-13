from bs4 import BeautifulSoup
import json
import os
import requests
import urllib2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dimsum_project.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from dimsum_app.config import *
from dimsum_app.models import *


def access_token():
    '''
    Get Yelp access token
    '''
    response = requests.post(ACCESS_TOKEN_URL, data={
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    return response.text


def populate_restaurants(params):
    '''
    Programmatically populate database with restaurants/menu items
    '''
    restaurants = json.loads(search_restaurants(params))
    for restaurant in restaurants['businesses']:
        print populate_restaurant(restaurant)


def search_restaurants(params):
    response = requests.get(SEARCH_URL, headers={
        'Authorization': AUTHORIZATION_HEADER
    }, params=params)
    return response.text


def populate_restaurant(restaurant):
    try:
        restaurant = Restaurant(id=restaurant['id'].encode('utf-8'),
                                name=restaurant['name'], description='',
                                rating=float(restaurant['rating']),
                                price_rating=int(len(restaurant['price'])),
                                location_string='',
                                longitude=float(
                                    restaurant['coordinates']['longitude']),
                                latitude=float(
                                    restaurant['coordinates']['latitude'])
                                )
        restaurant.save()
        populate_menu_items(restaurant, restaurant['id'].encode('utf-8'))
        return restaurant
    except KeyError:
        pass


def populate_menu_items(restaurant, restaurant_name):
    # Menu urls are of the form https://www.yelp.com/menu/**restaurant-name**
    restaurant_url = 'https://www.yelp.com/menu/{}'.format(restaurant_name)
    request = urllib2.Request(restaurant_url)
    response = urllib2.urlopen(request)
    # Skip if restaurant doesn't have menu
    if restaurant_url != response.geturl():
        return
    html = response.read()
    parsed_html = BeautifulSoup(html, 'lxml')
    for menu_item in parsed_html.find_all('div', class_='menu-item'):
        populate_menu_item(restaurant, menu_item)


def populate_menu_item(restaurant, menu_item):
    name = menu_item.find_all('h4')[0].get_text().strip()
    price = menu_item.find_all('div', 'menu-item-prices')[0].get_text().strip()
    try:
        dish = Dish(restaurant=restaurant, name=name,
                    price=float(price[1:]), description='', rating=0)
        dish.save()
    except ValueError:
        pass


if __name__ == '__main__':
    '''
    mountain_view_params = {'location': 'mountain-view'}
    populate_restaurants(mountain_view_params)
    '''
    pass
