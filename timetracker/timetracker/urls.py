from django.conf.urls import *

# allows for login/logout
from django.contrib.auth.views import login, logout

# helps load static files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from tracker.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timetracker.views.home', name='home'),
    # url(r'^timetracker/', include('timetracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),

    url(r'^$', index),
)


urlpatterns += staticfiles_urlpatterns()
