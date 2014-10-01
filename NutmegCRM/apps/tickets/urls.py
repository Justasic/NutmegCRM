from NutmegCRM.apps.tickets import views

__author__ = 'justasic'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.index),
    #url(r'^customer/[a-zA-Z0-9]+', views.customer)
    #url(r'', '')
)