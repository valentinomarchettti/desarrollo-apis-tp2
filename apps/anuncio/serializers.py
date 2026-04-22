from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from django.utils import timezone

from .models import Categoria, Anuncio


class CategoriaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Categoria
            fields = ['id', 'nombre', 'activa']


class AnuncioSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True,read_only=True)
    categorias_ids = PrimaryKeyRelatedField(queryset=Categoria.objects.all(),
                                            many=True,
                                            write_only=True,
                                            source='categorias')

    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'imagen',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',
            'categorias_ids',
            'publicado_por',
            'oferta_ganadora'
        ]
        read_only_fields= ['publicado_por', 'oferta_ganadora']

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        precio_inicial = data.get('precio_inicial')
        categorias = data.get('categorias')

        if fecha_inicio and fecha_inicio <= timezone.now():
            raise serializers.ValidationError({
                'fecha_inicio': 'La fecha de inicio debe ser posterior a la fecha actual.'
            })

        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
            })

        if precio_inicial is not None and precio_inicial <= 0:
            raise serializers.ValidationError({
                'precio_inicial': 'El precio inicial debe ser mayor a cero.'
            })

        if not categorias:
            raise serializers.ValidationError({
                'categorias_ids': 'Debe ingresar al menos una categoria.'
            })

        return data

    def create(self, validated_data):
        categorias = validated_data.pop('categorias')
        anuncio = Anuncio.objects.create(**validated_data)
        anuncio.categorias.set(categorias)
        return anuncio