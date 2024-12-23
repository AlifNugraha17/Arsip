# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path

from apps.home import views

from . import views
from .views import form_view


urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('form/', views.form_view, name='form'),
    path('form.html', views.form_view, name='form_html'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/change-password/<int:user_id>/', views.change_password, name='change_password'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
