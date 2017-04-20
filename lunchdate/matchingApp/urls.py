from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<person_id>[0-9]+)/$', views.queryOut, name='Query Output'),
    url(r'^(?P<person_id>[0-9]+)match/$', views.matchUser, name='MatchUser'),
    url(r'^(?P<person_id>[0-9]+)/matchnow/$', views.matchUserNow, name='MatchUserNow'),
    url(r'^(?P<person_id>[0-9]+)/addfriends/$', views.addFriends, name='addFriends'),
    url(r'^(?P<person_id>[0-9]+)/settings/$', views.settings, name='Settings'),
    url(r'^(?P<person_id>[0-9]+)/findrestaurant/$', views.findRestaurant, name='FindRestaurant'),

]