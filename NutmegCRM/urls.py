from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import urls as authurls

from NutmegCRM.apps.tickets import urls as ticketurls
from apps.crm import urls as crmurls
from django.contrib.auth import views as authviews

admin.autodiscover()

urlpatterns = [
    # Index for the entire site
    url(r'^$', 'NutmegCRM.apps.overview.views.index', name='home'),

    # our various apps for the site.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tickets/', include(ticketurls,  namespace='tickets')),
    url(r'^customers/', include(crmurls, namespace='customers')),
    url(r'^accounts/$', authviews.login),
    url(r'^accounts/', include(authurls)),
]
