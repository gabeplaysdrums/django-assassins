from django.conf.urls import patterns, include, url
from django.contrib import admin
import example.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^gamerules/(?P<gamerules_id>\d+)/$', example.views.gamerules_details)
)
