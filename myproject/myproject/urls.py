# filepath: c:\Users\pushk\Downloads\sneat-1.0.0\myproject\myproject\urls.py
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ipfs/', views.upload_view, name='ipfs_upload'),
    path('', views.home_view, name='home'),
]