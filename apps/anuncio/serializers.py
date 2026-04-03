from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

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

    def create(self, validated_data):
        categorias_data = validated_data.pop('categorias')
        anuncio = Anuncio.objects.create(**validated_data)

        for categoria_data in categorias_data:
            categoria_id = categoria_data.id
            if categoria_id:
                try:
                    categoria = Categoria.objects.get(id=categoria_id)
                    anuncio.categorias.add(categoria)
                except Categoria.DoesNotExist:
                    raise serializers.ValidationError({
                        "categorias_ids": [f"La categoría con id {categoria_id} no existe."]
                    })

        if not categorias_data:
            raise serializers.ValidationError({"categorias_ids": [f"Debe ingresar al menos una categoria."]})

        return anuncio