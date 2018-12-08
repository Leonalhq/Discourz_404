"""discourz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from django.urls import include
from discourz_app import views
from discourz_app.views import SearchView


urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('profile', views.profile, name='profile'),
    path('debate', views.debate, name='debate'),
    path('waitLobby/<slug:id>/', views.waitLobby, name='waitLobby'),
    path('joinChat/<slug:uuid>/', views.joinChat, name='joinChat'),
    path('debateChat/<slug:uuid>/', views.debateChat, name='debateChat'),
    path('debate_create', views.debate_create, name='debate_create'),
    path('pastChat/<slug:uuid>/', views.pastChat, name='pastChat'),
    path('edit_profile/<slug:username>',views.edit_profile, name='edit_profile'),
    path('poll_home', views.poll_home, name='poll_home'),
    path('poll_create', views.poll_create, name='poll_create'),
    path('poll/<slug:uuid>/', views.poll, name='poll'),
    path('poll_voting/<slug:uuid>/<slug:vote>/', views.poll_voting, name='poll_voting'),
    path('poll_deleting/<slug:uuid>/', views.poll_deleting, name='poll_deleting'),
    #path('poll', views.poll, name='poll'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    path('discussion', views.discussion, name='discussion'),
    url(r'^ajax/create_past_debate/$', views.create_past_debate, name='create_past_debate'),
    url(r'^ajax/post_comment/$', views.post_comment, name='post_comment'),
]