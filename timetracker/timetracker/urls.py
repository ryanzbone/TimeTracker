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
    url(r'^accounts/logout/$', logout, name='auth_logout'),

    url(r'^all/$', all_entries, name='all_entries'),
    url(r'^today/$', today, name='today'),
    url(r'^date/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', date, name='date'),
    url(r'^start/(?P<entry>\d+)/$', start_task, name='start_task'),
    url(r'^stop/(?P<entry>\d+)/$', stop_task, name='stop_task'),
    url(r'^billing/$', billing, name='billing'),
    url(r'^billing/(?P<customer>[^/]+)/$', customer_billing, name='customer_billing'),
    url(r'^form/add/(?P<formType>[^/]+)/$', add_form, name='add_form'),
    
    url(r'^form/update/(?P<entryId>\d+)/$', update_form, name='update_form'),

    url(r'^csv/choose/$', choose_csv, name='choose_csv'),
    url(r'^csv/export/(?P<entryId>\d+)/$', export_csv, name='export_csv'),


)


urlpatterns += staticfiles_urlpatterns()
