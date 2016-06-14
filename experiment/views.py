from django.shortcuts import render, redirect
from django.http import HttpResponse
from waiting_room import views



def home_page(request):
    return render(request,'experiment/home.html')

def finish(request):
    return render(request,'experiment/finish.html')

def survey(request):
    return render(request,'experiment/survey.html')

def wait_room(request):
    return render(request,'waiting_room/wait_home.html')
    

def forumapp(request):
    return render(request,'forum/about.html')

def chatapp(request):
    return render(request,'chat/about.html')


