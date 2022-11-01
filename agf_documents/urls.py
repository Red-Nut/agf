"""agf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from . import views

urlpatterns = [
    # Document Dashboard
    path('', views.IndexLogin.as_view(), name='documents'),

    # Document Page
    path('document/<int:id>/', views.DocumentPage, name='document'),
    path('document_new_revision/<int:id>/', views.NewDocumentRevision, name='document_new_revision'),
    path('document_new_reference/<int:id>/', views.NewDocumentReference, name='document_new_reference'),

    # Document Search
    path('search', views.Search, name='document_search'),

    # Create new Document
    path('create', views.Create, name='document_create'),
    

    # Admin Functions
    path('missing_files', views.MissingFiles), 
]
