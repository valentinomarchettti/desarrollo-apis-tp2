from django.urls import path

from .api import (
    AnuncioDetalleAPIView,
    AnuncioListaAPIView,
    CategoriaDetalleAPIView,
    CategoriaListaAPIView,
)


app_name = 'anuncio_v1'

urlpatterns = [
    path('categoria/', CategoriaListaAPIView.as_view()),
    path('categoria/<int:pk>/', CategoriaDetalleAPIView.as_view()),
    path('anuncio/', AnuncioListaAPIView.as_view()),
    path('anuncio/<int:pk>/', AnuncioDetalleAPIView.as_view()),
]
