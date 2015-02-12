from django.conf.urls import patterns, include, url
from apps.main.urls import main_urls
from apps.messaging.urls import messaging_urls
from apps.parceadores.urls import parceadores_urls
from apps.tags.urls import tags_urls
from apps.userManager.urls import userManager_urls
from apps.oauthSocial.urls import oauthSocial_urls
from django.conf import settings

from django.contrib import admin


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(main_urls)),
    url(r'^oauth/', include(oauthSocial_urls)),
   	url(r'^', include(userManager_urls)),   
    url(r'^api/', include(messaging_urls)),
    url(r'^api/', include(tags_urls)),
    url(r'^api/', include(parceadores_urls)),
)

urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),)
