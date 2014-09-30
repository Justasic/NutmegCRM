__author__ = 'justasic'
from django.conf.urls import patterns, url

from NutmegCRM.apps.crm import views


urlpatterns = patterns('',
    url(r'^$', views.index),
    #url(r'', '')
)