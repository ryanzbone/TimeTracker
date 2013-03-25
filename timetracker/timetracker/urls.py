from django.conf.urls import *

# allows for login/logout
from django.contrib.auth.views import login, logout

# helps load static files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from tracker.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Admin pages
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # Login/Logout
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, name='auth_logout'),

    # View work entries
    url(r'^all/$', all_entries, name='all_entries'),
    url(r'^today/$', today, name='today'),
    url(r'^date/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', date, name='date'),

    #Start or stop WorkEntry WorkDurations
    url(r'^start/(?P<entry>\d+)/$', start_task, name='start_task'),
    url(r'^stop/(?P<entry>\d+)/$', stop_task, name='stop_task'),

    # Billing Info
    url(r'^billing/$', billing, name='billing'),
    url(r'^billing/(?P<customer>[^/]+)/$', customer_billing, name='customer_billing'),
    
    # Add, update forms
    url(r'^form/add/(?P<formType>[^/]+)/$', add_form, name='add_form'),
    url(r'^form/update/(?P<entryId>\d+)/$', update_form, name='update_form'),

    # CSV selection, export
    url(r'^csv/choose/$', choose_csv, name='choose_csv'),
    url(r'^csv/export/(?P<entryId>\d+)/$', export_csv, name='export_csv'),

    # Used for chained-selects in Add/Update forms
    url(r'^chaining/', include('smart_selects.urls')),
)

urlpatterns += staticfiles_urlpatterns()