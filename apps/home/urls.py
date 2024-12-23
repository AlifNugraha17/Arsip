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
    path('delete/<int:dokumen_id>/', views.delete_dokumen, name='delete_dokumen'),
    path('edit/<int:dokumen_id>/', views.edit_dokumen, name='edit_dokumen'),
    

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
