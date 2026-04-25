from django_filters import rest_framework as filters

from .models import Anuncio, Categoria


class CategoriaFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        model = Categoria
        fields = ['nombre', 'activa']


class AnuncioFilter(filters.FilterSet):
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains')
    precio_min = filters.NumberFilter(field_name='precio_inicial', lookup_expr='gte')
    precio_max = filters.NumberFilter(field_name='precio_inicial', lookup_expr='lte')
    fecha_inicio_desde = filters.DateTimeFilter(field_name='fecha_inicio', lookup_expr='gte')
    fecha_fin_hasta = filters.DateTimeFilter(field_name='fecha_fin', lookup_expr='lte')

    class Meta:
        model = Anuncio
        fields = [
            'titulo',
            'activo',
            'categorias',
            'publicado_por',
        ]
