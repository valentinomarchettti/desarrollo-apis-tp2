from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import AnuncioViewSet, OfertaAnuncioCreateAPIView


app_name = 'anuncio_api'

router = DefaultRouter()
router.register(prefix='anuncios', viewset=AnuncioViewSet, basename='anuncio')

urlpatterns = [
    path(
        'anuncios/<uuid:anuncio_uuid>/ofertas/',
        OfertaAnuncioCreateAPIView.as_view(),
        name='anuncio-ofertas',
    ),
    path('', include(router.urls)),
]
