from __future__ import unicode_literals
import random

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey

import search


class Restaurant(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rating = models.DecimalField(decimal_places=2, max_digits=3)
    price_rating = models.DecimalField(decimal_places=2, max_digits=3)
    location_string = models.CharField(max_length=100)
    longitude = models.DecimalField(decimal_places=6, max_digits=9)
    latitude = models.DecimalField(decimal_places=6, max_digits=9)

    def __str__(self):
        return u'{}'.format(self.name)

    def indexing(self):
        obj = RestaurantIndex(
            name=self.name,
            rating=self.rating,
            price_rating=self.price_rating,
            location_string=self.location_string,
            longitude=self.longitude,
            latitude=self.latitude
        )
        obj.save()
        return obj.to_dict()


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=1000)
    rating = models.DecimalField(decimal_places=2, max_digits=3)

    class Meta:
        abstract = True

    def __str__(self):
        return u'{} from {}'.format(self.name, self.restaurant.name)


class Dish(MenuItem):

    def indexing(self):
        obj = search.DishIndex(
            restaurant=self.restaurant.name,
            name=self.name,
            price=self.price,
            description=self.description,
            rating=self.rating
        )
        obj.save()
        return obj.to_dict()


class Drink(MenuItem):
    pass


class Review(models.Model):
    dish = models.ForeignKey(Dish)
    review = models.CharField(max_length=1000)
    rating = models.PositiveIntegerField()


class Photo(models.Model):
    dish = models.ForeignKey(Dish)
    image = models.ImageField()
    description = models.CharField(max_length=1000)


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    salt = models.CharField(max_length=50)
    hashed_password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
