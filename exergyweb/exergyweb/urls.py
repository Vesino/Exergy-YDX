"""exergyweb URL Configuration

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
from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from exergyapp import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.index),
    path('', include('exergyapp.urls')),
    path('forecast/', v.pvlib_location, name="Forecasting"),
    #path('sky_cam/', v.sky_cam, name='Sky-cam-images'),
    path('download_data', v.all_folders),
    path('chart', v.pvlib_location, name='chart'),
    path('download_folder/',v.download_folder,name="download_folder"),
    url('download_my_forecasts', v.download_forecasts),
]

urlpatterns += staticfiles_urlpatterns()
