from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    #url(r'^chats/', views.home_page, name='home_page'),
    url(r'^waitapp/',views.wait_room,name='waiting_room'),
    url(r'^chatapp/',views.chatapp,name='chatapp'),
    url(r'^forumapp/',views.forumapp,name='forumapp'),
    url(r'^survey/',views.survey,name='survey'),
    url(r'^finish/',views.finish,name='finish'),
]
