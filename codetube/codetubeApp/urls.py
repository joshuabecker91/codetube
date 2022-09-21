from django.urls import path, re_path
from . import views
from django.conf import settings 


urlpatterns = [
    # General Routes:
    path('', views.index), # no login needed
    path('results/', views.search), # no login needed # need to enter path param string
    path('popular_videos/', views.popular_videos),
    # User Routes:
    path('login_reg/', views.login_reg),
    path('login/', views.login),
    path('register/', views.register),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout),
    # Video Routes:
    path('play/<int:id>', views.play_video), # no login needed
    path('new_video/', views.new_video),
    path('create_video/', views.create_video),
    path('edit_video/<int:id>', views.edit_video),
    path('update_video/<int:id>', views.update_video),
    path('delete_video/<int:id>', views.delete_video),
    # Like Routes:
    path('like_video/<int:id>', views.like_video),
    path('user_liked/', views.user_liked),
    # Test Routes:
    # path('testlogin_reg/', views.testlogin_reg),
    # path('testdashboard/', views.testdashboard),
]

# If you want to be able to update user, reference ------------------------
    # path('myaccount/<int:id>', views.account_page),
    # path('user/<int:id>', views.user_page),