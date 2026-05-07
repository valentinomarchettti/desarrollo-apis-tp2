from django.contrib import admin
from .models import Anuncio, Categoria, OfertaAnuncio, SeguimientoAnuncio


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre',)


@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'titulo', 'precio_inicial', 'activo', 'publicado_por', 'fecha_inicio', 'fecha_fin')
    list_filter = ('activo', 'categorias')
    search_fields = ('uuid', 'titulo', 'publicado_por__username')
    filter_horizontal = ('categorias',)
    readonly_fields = ('uuid', 'fecha_publicacion')


@admin.register(OfertaAnuncio)
class OfertaAnuncioAdmin(admin.ModelAdmin):
    list_display = ('id', 'anuncio', 'usuario', 'precio_oferta', 'fecha_oferta', 'es_ganador')
    list_filter = ('es_ganador', 'fecha_oferta')
    search_fields = ('anuncio__titulo', 'usuario__username')
    readonly_fields = ('fecha_oferta',)


@admin.register(SeguimientoAnuncio)
class SeguimientoAnuncioAdmin(admin.ModelAdmin):
    list_display = ('id', 'anuncio', 'usuario', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('anuncio__titulo', 'usuario__username')
    readonly_fields = ('fecha',)
