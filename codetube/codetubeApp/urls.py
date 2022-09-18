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
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    # Video and Like Routes:
    # path('create/<int:id>', views.create),
    # path('update/<int:id>', views.update),
    # path('delete/<int:id>', views.delete),
    # path('like', views.like),
    # Test Routes:
    # path('testlogin_reg/', views.testlogin_reg),
    # path('testdashboard/', views.testdashboard),
]



# other
    # path('myaccount/<int:id>', views.account_page),
    # path('user/<int:id>', views.user_page),

# Reference, full from project
# urlpatterns = [
#     path('', views.index),
#     path('register', views.register),
#     path('login', views.login),
#     path('logout', views.logout),
#     path('success', views.success),
#     path('add_quote', views.add_quote),
#     path('myaccount/<int:id>', views.account_page),
#     path('update/<int:id>', views.update),
#     path('user/<int:id>', views.user_page),
#     path('like', views.like),
#     path('delete/<int:id>', views.delete)
# ]