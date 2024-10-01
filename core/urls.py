from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginSSO, name='loginSSO'), 
    path('laman-admin/', include('admin_notulensi.urls')),
    path('accounts/', include('allauth.urls')),
]
