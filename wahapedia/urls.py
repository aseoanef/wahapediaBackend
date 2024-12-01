"""
URL configuration for wahapedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from warhammer import endpoints

urlpatterns = [
    path('admin/', admin.site.urls),
    path('army/',endpoints.army),
    path('army/<int:armyId>/',endpoints.armybyId),
    path('operative/', endpoints.operative),
    path('operative/<int:operativeId>/', endpoints.operativebyId),
    path('gun/', endpoints.gun),
    path('gun/<int:gunId>/', endpoints.gunbyId),
    path('attack/<int:gunId>/', admin.site.urls),
    path('uniqueaction/', endpoints.uniqueaction),
    path('uniqueaction/<int:uniqueactionId>/', endpoints.uniqueactionbyId),
    path('specialrule/', endpoints.specialrule),
    path('specialrule/<int:specialruleId>/', endpoints.specialrulebyId),
    path('ability/', endpoints.ability),
    path('ability/<int:abilityId>/', endpoints.abilitybyId),
    path('customarmy/', endpoints.getcustomarmy),
    path('customarmy/<int:customarmyId>/', endpoints.customarmy), #get put delete post
    path('operativegun/', endpoints.getcustomopp),
    path('operativegun/<int:operativegunId>/', endpoints.customopp), #post get put delete post
]
