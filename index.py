from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Text, Float, Search
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk

'''
Script to create indices
'''


def bulk_index_dishes():
    DishIndex.init()
    es = Elasticsearch()
    # TODO: why is _id: 1 needed to prevent duplicate entries?
    bulk(client=es, actions=[{'_index': 'dish-index', '_type': 'dish_index', '_id': 1,
                              '_source': dish.indexing()} for dish in models.Dish.objects.all().iterator()])

if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dimsum_project.settings')
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from dimsum_app import models
    from dimsum_app.search import DishIndex

    connections.create_connection()
    bulk_index_dishes()
