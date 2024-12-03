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
    path('admin/', admin.site.urls), #editar la pantalla de admin en admin.py
    path('army/',endpoints.army), # POST GET
    path('army/<int:armyId>/',endpoints.armybyId), #GET PUT
    path('operative/', endpoints.operative), #GET POST
    path('operative/<int:operativeId>/', endpoints.operativebyId), #GET PUT
    path('gun/', endpoints.gun), #GET POST
    path('gun/<int:gunId>/', endpoints.gunbyId), #GET PUT
    path('attack/<int:gunId>/', endpoints.attack), #GET
    path('uniqueaction/', endpoints.uniqueaction), #GET POST
    path('uniqueaction/<int:uniqueactionId>/', endpoints.uniqueactionbyId), #GET PUT
    path('specialrule/', endpoints.specialrule), #GET POST
    path('specialrule/<int:specialruleId>/', endpoints.specialrulebyId), #GET PUT
    path('ability/', endpoints.ability), #GET POST
    path('ability/<int:abilityId>/', endpoints.abilitybyId), #GET PUT
    path('customarmy/', endpoints.getcustomarmy), #GET POST
    path('customarmy/<int:customarmyId>/', endpoints.customarmy), #GET PUT DELETE
    path('operativegun/', endpoints.getcustomopp), #GET POST
    path('operativegun/<int:operativegunId>/', endpoints.customopp), #GET PUT DELETE
]
