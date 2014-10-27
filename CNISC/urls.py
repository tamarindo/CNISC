from django.conf.urls import patterns, include, url
from apps.main.urls import main_urls
from apps.messaging.urls import messaging_urls
from apps.parceadores.urls import parceadores_urls
from apps.tags.urls import tags_urls
from apps.userManager.urls import userManager_urls
from apps.oauthSocial.urls import oauthSocial_urls

from django.contrib import admin


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(main_urls)),
    url(r'^oauth/', include(oauthSocial_urls)),
    url(r'^', include(messaging_urls)),
    url(r'^tags/', include(tags_urls)),
    url(r'^parce/', include(parceadores_urls)),
    url(r'^', include(userManager_urls)),

)
