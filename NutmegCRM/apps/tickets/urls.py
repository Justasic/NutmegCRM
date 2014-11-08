from NutmegCRM.apps.tickets import views

__author__ = 'justasic'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^(?P<custid>\d+)/(?P<lastname>[\-\W]+)/(?P<firstname>[\-\W]+)/', views.customer),
    url(r'^(?P<custid>\d+)/(?P<lastname>[\-\W]+)/(?P<firstname>[\-\W]+)/(?P<invoiceid>\d+)/', views.ticket),
    #url(r'', '')
)