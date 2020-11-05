from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index),
    #path('', include('exergyapp.urls')),
]

urlpatterns += staticfiles_urlpatterns()
