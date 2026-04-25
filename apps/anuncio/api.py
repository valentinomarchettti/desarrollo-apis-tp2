from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from rest_framework.generics import (get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from .models import Categoria, Anuncio
from .filters import CategoriaFilter, AnuncioFilter
from .serializers import CategoriaSerializer, AnuncioSerializer
from django.shortcuts import get_object_or_404

from ..usuario.models import Usuario

SEGUNDOS_POR_MINUTO = 60
MINUTOS_POR_HORA = 60
HORAS_POR_DIA = 24
SEGUNDOS_POR_HORA = SEGUNDOS_POR_MINUTO * MINUTOS_POR_HORA
SEGUNDOS_POR_DIA = SEGUNDOS_POR_HORA * HORAS_POR_DIA


# Vistas para Categorias
class CategoriaListaAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaDetalleAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=pk)  # Sin espacio antes del (
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Vistas para Anuncios
class AnuncioListaAPIView(APIView):
    def get(self, request, *args, **kwargs):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AnuncioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(publicado_por=get_object_or_404(Usuario, id=1))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnuncioDetalleAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# GenericView
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


# Generic view anuncio

class AnuncioListaGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def perform_create(self, serializer):
        serializer.save(publicado_por=get_object_or_404(Usuario, id=1))


class AnuncioDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer


# ViewSet
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre', 'id']


# Anuncio viewset
class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnuncioFilter
    ordering_fields = [
        'titulo',
        'precio_inicial',
        'fecha_inicio',
        'id',
    ]

    def perform_create(self, serializer):
        serializer.save(publicado_por=get_object_or_404(Usuario, id=1))

    @action(detail=True, methods=['get'], url_path='tiempo-restante')
    def tiempo_restante(self, request, pk=None):
        anuncio = self.get_object()

        if anuncio.fecha_fin is None:
            return Response(
                {'detail': 'El anuncio no tiene fecha_fin definida.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ahora = timezone.now()
        diferencia = anuncio.fecha_fin - ahora

        if diferencia.total_seconds() <= 0:
            return Response(
                {
                    'anuncio_id': anuncio.id,
                    'finalizado': True,
                    'tiempo_restante': {
                        'dias': 0,
                        'horas': 0,
                        'minutos': 0
                    }
                },
                status=status.HTTP_200_OK
            )

        total_segundos = int(diferencia.total_seconds())

        #(divmod)Función que guarda el cociente entero, y el resto de la división
        dias, resto = divmod(total_segundos, SEGUNDOS_POR_DIA)
        horas, resto = divmod(resto, SEGUNDOS_POR_HORA)
        minutos = resto // SEGUNDOS_POR_MINUTO

        return Response(
            {
                'anuncio_id': anuncio.id,
                'finalizado': False,
                'tiempo_restante': {
                    'dias': dias,
                    'horas': horas,
                    'minutos': minutos
                }
            },
            status=status.HTTP_200_OK
        )
