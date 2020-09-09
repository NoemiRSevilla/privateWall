from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^postmessage$', views.postmessage),
    url(r'^postcomment$', views.postcomment),
    url(r'^message/(?P<id>\d+)/delete', views.delete)
]