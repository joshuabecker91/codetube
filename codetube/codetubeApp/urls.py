from django.urls import path
from . import views
from django.conf import settings 


urlpatterns = [
    path('', views.index),
    path('search/', views.search),
    path('login_reg/', views.login_reg),
    path('dashboard/', views.dashboard),
    path('new_video/', views.new_video),
    path('edit_video/', views.edit_video),
    path('play/', views.play),
]