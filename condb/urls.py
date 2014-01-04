from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret

urlpatterns = patterns('',
    if_installed('labour', r'^labour/', include('labour.urls')),
    if_installed('programme', r'^programme/', include('programme.urls')),
    (r'^admin/', include(admin.site.urls)),
)