# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path

from apps.home import views

from . import views

#from .views import form_view, index_view


urlpatterns = [
    # Halaman form
    path('form/', views.form_view, name='form'),
    path('form.html', views.form_view, name='form_html'),  # Alternatif URL untuk form.html

    # Halaman profile
    path('profile/', views.profile_view, name='profile'),
    path('profile.html', views.profile_view, name='profile_html'),  # Alternatif URL untuk profile.html

    # Halaman index
    path('', views.index, name='index'),

    # Halaman dinamis (untuk menangani halaman selain yang sudah ditentukan di atas)
    re_path(r'^(?P<page_name>[a-zA-Z0-9_-]+)/?$', views.pages, name='pages'),
]

