from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signout$', views.signout, name='signout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^change_password$', views.change_password, name='change_password'),
    url(r'^register$', views.register, name='register'),

    url(r'^search$', views.searchResults, name='search'),
]
