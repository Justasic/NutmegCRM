from NutmegCRM.apps.tickets import views

__author__ = 'justasic'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<custid>\d+)/(?P<lastname>[\-\W]+)/(?P<firstname>[\-\W]+)/', views.customer, name='customer'),
    url(r'^(?P<invoiceid>\d+)/', views.ticket, name='ticket'),
    #url(r'', '')
)