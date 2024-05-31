"""
URL configuration for Project2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static
from app import views as app_views,views
from authentication import views
# from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('app/', include('app.urls')),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', app_views.dashboard, name='dashboard'),
    # path('^dashboard/$', views.dashboard, name='dashboard'),

    path('^login/$', views.login, name='login'),  # Your custom login view
    path('^logout/$', views.logout_view, name='logout'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)