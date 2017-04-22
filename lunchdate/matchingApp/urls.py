from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<person_id>[0-9]+)/$', views.queryOut, name='Query Output'),
    url(r'^(?P<person_id>[0-9]+)/matchnow/(?P<distance>[0-9]+)/(?P<hour>[0-9]+|-)/(?P<minute>[0-9]+|-)/(?P<day>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|-)/$', views.matchUserNow, name='MatchUserNow'),
    url(r'^(?P<person_id>[0-9]+)/addfriends/$', views.addFriends, name='addFriends'),
    url(r'^(?P<person_id>[0-9]+)/settings/$', views.settings, name='Settings'),
    url(r'^(?P<person_id>[0-9]+)/findrestaurant/$', views.findRestaurant, name='FindRestaurant'),
	url(r'^(?P<fr_id>[0-9]+)matchedrestaurant/(?P<person_id>[0-9]+)/(?P<day>[0-9]+)/(?P<time>[0-9]+)/(?P<dist>[0-9]+)/$', views.getMatchRestaurant, name='MatchRestaurant'),
	url(r'^(?P<person_id>[0-9]+)/addfriends/(?P<fr_id>[0-9]+)/$', views.friendEntry, name='FriendEntry'),
	url(r'^(?P<person_id>[0-9]+)/queryrestaurant/(?P<foodtype>.*)/(?P<dist>[0-9]+)/(?P<hour>[0-9]+|-)/(?P<minute>[0-9]+|-)/(?P<day>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|-)/$', views.queryRestaurant, name='QueryRestaurant'),
	url(r'^(?P<person_id>[0-9]+)/update/(?P<newname>.*)/(?P<mealplan>T|F|N)/(?P<strangers>T|F|N)/$', views.updateUser, name='UpdateUser'),
	]