
from django.urls import path, include
from django.contrib.auth import views as auth_views

from authentication import views
from .views import logout_view
from django.urls import path
from .views import register,login
urlpatterns = [
    path('register/', register, name='register'),
    path('',login, name='login'),
    # # path('logout/', logout_view, name='logout'),
    # path('logout/', views.logout_view, name='logout'),



]
