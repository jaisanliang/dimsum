from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Text, Float, Search
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk

'''
ElasticSearch module

Guide for integrating Django and ElasticSearch:
https://medium.freecodecamp.org/elasticsearch-with-django-the-easy-way-909375bc16cb
'''


class DishIndex(DocType):
    restaurant_name = Text()
    restaurant_id = Text()
    name = Text()
    price = Float()
    description = Text()
    rating = Float()

    class Meta:
        index = 'dish-index'


def search_dishes(dish):
    connections.create_connection()
    search = Search().query('match', name=dish)
    num_results = search.count()
    search = search[0:num_results]
    response = search.execute()
    return response
