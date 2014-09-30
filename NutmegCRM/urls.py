from django.conf.urls import patterns, include, url
from django.contrib import admin

from NutmegCRM.apps.tickets import urls as ticketurls
from apps.crm import urls as crmurls

admin.autodiscover()

urlpatterns = patterns('',
    # Index for the entire site
    url(r'^$', 'NutmegCRM.apps.overview.views.index', name='home'),

    # our various apps for the site.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tickets/', include(ticketurls)),
    url(r'^customers/', include(crmurls)),
)
