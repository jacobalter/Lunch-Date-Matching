from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<person_id>[0-9]+)/$', views.queryOut, name='Query Output'),
    url(r'^(?P<person_id>[0-9]+)match/$', views.matchUser, name='MatchUser'),
    url(r'^(?P<person_id>[0-9]+)/matchnow/$', views.matchUserNow, name='MatchUserNow'),
]