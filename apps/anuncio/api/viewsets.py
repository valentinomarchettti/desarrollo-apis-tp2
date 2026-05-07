from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from ..filters import AnuncioFilter, CategoriaFilter
from ..models import Anuncio, Categoria, OfertaAnuncio
from .permissions import IsOwnerOfAnuncio, StrictModelPermissions
from .serializers import AnuncioSerializer, CategoriaSerializer, OfertaAnuncioSerializer


SEGUNDOS_POR_MINUTO = 60
MINUTOS_POR_HORA = 60
HORAS_POR_DIA = 24
SEGUNDOS_POR_HORA = SEGUNDOS_POR_MINUTO * MINUTOS_POR_HORA
SEGUNDOS_POR_DIA = SEGUNDOS_POR_HORA * HORAS_POR_DIA


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre', 'id']


class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    permission_classes = [StrictModelPermissions, IsOwnerOfAnuncio]
    lookup_field = 'uuid'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnuncioFilter
    ordering_fields = [
        'titulo',
        'precio_inicial',
        'fecha_inicio',
        'uuid',
    ]

    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)

    @action(detail=True, methods=['get'], url_path='tiempo-restante')
    def tiempo_restante(self, request, uuid=None):
        anuncio = self.get_object()

        if anuncio.fecha_fin is None:
            return Response(
                {'detail': 'El anuncio no tiene fecha_fin definida.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ahora = timezone.now()
        diferencia = anuncio.fecha_fin - ahora

        if diferencia.total_seconds() <= 0:
            return Response(
                {
                    'anuncio_uuid': str(anuncio.uuid),
                    'finalizado': True,
                    'tiempo_restante': {
                        'dias': 0,
                        'horas': 0,
                        'minutos': 0,
                    },
                },
                status=status.HTTP_200_OK,
            )

        total_segundos = int(diferencia.total_seconds())
        dias, resto = divmod(total_segundos, SEGUNDOS_POR_DIA)
        horas, resto = divmod(resto, SEGUNDOS_POR_HORA)
        minutos = resto // SEGUNDOS_POR_MINUTO

        return Response(
            {
                'anuncio_uuid': str(anuncio.uuid),
                'finalizado': False,
                'tiempo_restante': {
                    'dias': dias,
                    'horas': horas,
                    'minutos': minutos,
                },
            },
            status=status.HTTP_200_OK,
        )


class OfertaAnuncioCreateAPIView(generics.CreateAPIView):
    queryset = OfertaAnuncio.objects.all()
    serializer_class = OfertaAnuncioSerializer
    permission_classes = [StrictModelPermissions]

    def get_anuncio(self):
        return get_object_or_404(Anuncio, uuid=self.kwargs['anuncio_uuid'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['anuncio'] = self.get_anuncio()
        return context

    def create(self, request, *args, **kwargs):
        anuncio = self.get_anuncio()

        if anuncio.publicado_por_id == request.user.id:
            raise PermissionDenied('El creador del anuncio no puede realizar ofertas sobre su propio anuncio.')

        if not anuncio.activo:
            raise ValidationError({'anuncio': 'El anuncio no se encuentra activo.'})

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        anuncio = self.get_anuncio()
        serializer.save(anuncio=anuncio, usuario=self.request.user)
