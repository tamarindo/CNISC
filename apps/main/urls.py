from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

main_urls = patterns('apps.main.views',
	url(r'^changetypev$', 'changeTypeVisualization', name="changeTypeVisualization"),
	url(r'^seenmessage$', 'seenMessage', name="seenMessage"),
	url(r'^getmessage$', 'getMessage', name="getMessage"),
    url(r'^logout$', 'v_logout', name="v_logout"),
    url(r'^login/$','login', name="login"),
    url(r'^$','home', name="home"),    
)  


