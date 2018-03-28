from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.success),
    url(r'^travels/add$', views.add),
    url(r'^travels/create$', views.create),
    url(r'^travels/join/(?P<id>\d+)', views.join),
    url(r'^travels/destination/(?P<id>\d+)$', views.show)
    # url(r'^contribute$', views.contribute),
    # url(r'^add$', views.add),
    # url(r'^remove$', views.remove),
    # url(r'^users/(?P<id>\d+)$', views.show),
]
