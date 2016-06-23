from django.conf.urls import include, url
#from . import chat.views
import chat.views

urlpatterns = [
    url(r'^$',  chat.views.about, name='about'),
    url(r'^new/$', chat.views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', chat.views.chat_room, name='chat_room'),
]
