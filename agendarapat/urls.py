from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_agenda, name='create_agenda'),
    path('<int:pk>/', views.detail_agenda, name='detail_agenda'),
    path('<int:pk>/notulen/', views.create_notulen, name='create_notulen'),
    path('fetch-employees/', views.fetch_employees, name='fetch_employees'),    
    path('list/', views.list_agenda, name='list_agenda'),
]
