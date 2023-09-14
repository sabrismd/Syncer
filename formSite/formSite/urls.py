"""
URL configuration for formSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from formApp import views

urlpatterns = [
    path('',views.home),
    path('admin', admin.site.urls),
    path('display_token', views.display_token),
    path('sheet_user',views.display_sheet_user),
    path('server_details',views.server_details),
    path('server_connection_status',views.server_connection),
    path('database_details',views.tables),
    path('selected',views.selected),
    path('confirm_sync',views.matching),
    path('merge',views.sync),
    path('create_sheet',views.create_sheet),
    path('createsheetworkspace',views.sheetinworkspace),
    path('createsheetsheets',views.sheetinsheets),
    path('close/',views.closetab),
]


