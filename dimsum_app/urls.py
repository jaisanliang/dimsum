from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^register$', views.register, name='register'),
    url(r'^search$', views.searchResults, name='search'),
]
