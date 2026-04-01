from django.urls import path
from .api import CategoriaListaAPIView, CategoriaDetalleAPIView
app_name= 'anuncio'

urlpatterns = [
    path('api-view/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<int:pk>/', CategoriaDetalleAPIView.as_view()),
]