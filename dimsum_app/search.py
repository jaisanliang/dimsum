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
    restaurant = Text()
    name = Text()
    price = Float()
    description = Text()
    rating = Float()

    class Meta:
        index = 'dish-index'


def search_dishes(dish):
    connections.create_connection()
    search = Search().filter('term', name=dish)
    response = search.execute()
    return response


def bulk_index_dishes():
    DishIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=[{'_index': 'dish-index', '_type': 'dish',
                              '_source': dish.indexing()} for dish in models.Dish.objects.all().iterator()])

if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dimsum_project.settings')
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    import models

    connections.create_connection()
