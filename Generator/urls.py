"""SFIAGenerator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='form_page'),
    path('search/', views.search_page, name='search_page'),
    path('list/', views.list_skills, name='list_skills_page'),
    path('skill/<slug:code>/', views.show_skill, name='show_skill_page'),
    path('select/<slug:code_1>/', views.select_second, name='select_second'),
    path('select/<slug:code_1>/<slug:code_2>/', views.view_second, name='view_second'),
    path('language_preferences/', views.language_preferences_page, name='language_preferences_page')
]
