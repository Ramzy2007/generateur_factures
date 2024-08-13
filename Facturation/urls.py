from django.contrib import admin
from django.urls import path, include
from client import views as client_views  # Import the client views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('client.urls')),
    path('produits/', include('produit.urls')),
    path('', client_views.client_list, name='client_list'),  # Use the imported home view
]