from django.conf.urls import patterns, include, url
from apps.main.urls import main_urls
from apps.oauthSocial.urls import oauthSocial_urls

from django.contrib import admin


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(main_urls)),
    url(r'^oauth/', include(oauthSocial_urls)),
)
