"""funkoSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from inventory import views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    path('users/', include('users.urls')),
    path('inventory/', include('inventory.urls')),
    path('system_tailoring/', views.SystemTailoring.as_view(), name='system_tailoring'),
    path('about/', views.AboutView.as_view(), name='about'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('welcome_admin/', views.WelcomeAdminView.as_view(), name='welcome_admin'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)