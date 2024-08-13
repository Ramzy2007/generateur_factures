from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_client, name='create_client'),
    path('<int:pk>/', views.client_detail, name='client_detail'),
]
