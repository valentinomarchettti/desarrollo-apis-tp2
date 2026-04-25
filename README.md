# Subastas Clase

Proyecto realizado con Django y Django REST Framework para exponer una API orientada a la gestion de categorias y anuncios dentro de una plataforma de subastas.

## Alcance de este README

Este documento resume el historial real revisado en git para que el contenido del repositorio y su evolucion queden alineados.

- Commits y merges observados en el historial: commit inicial, PR #1, PR #2, PR #3, PR #5 y PR #6.
- No se observa un merge de PR #4 en el historial consultado.
- El PR #6 aparece mergeado en `origin/main`, por eso se incluye en este resumen historico.

## Estructura principal

- `apps/anuncio/`: modelos, serializers y endpoints de categorias y anuncios.
- `apps/usuario/`: modelo base de usuario usado por los anuncios y ofertas.
- `subastas_clase/`: configuracion del proyecto Django, URLs globales y router de DRF.
- `docs/pruebas_postman.png`: evidencia de pruebas manuales sobre endpoints.

## Historial de commits y pull requests

### Commit inicial - `57d8e0b`

Se creo la base del proyecto Django y la estructura de aplicaciones.

Cambios principales:
- Creacion del proyecto `subastas_clase`.
- Alta de las apps `anuncio` y `usuario`.
- Definicion de modelos iniciales para categorias, anuncios, ofertas y seguimiento.
- Generacion de migraciones iniciales.
- Alta de `manage.py` y `db.sqlite3`.

Archivos relevantes creados:
- `manage.py`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`
- `apps/anuncio/models.py`
- `apps/usuario/models.py`
- `apps/anuncio/migrations/0001_initial.py`
- `apps/usuario/migrations/0001_initial.py`

### PR #1 - `feature/Paula` - merge `9c111b1`

Commit del branch:
- `0f27d27`: `Categoria completo`

Cambios incorporados:
- Se agrego Django REST Framework a `INSTALLED_APPS`.
- Se configuro `REST_FRAMEWORK` con renderers JSON y Browsable API.
- Se creo `apps/anuncio/api.py` con CRUD de `Categoria` usando `APIView`.
- Se creo `apps/anuncio/url.py` y se montaron las rutas en `subastas_clase/urls.py`.
- Se creo `apps/anuncio/serializers.py` con `CategoriaSerializer` y una version base de `AnuncioSerializer`.
- Se ajusto `__str__` en `Anuncio`.
- Se agrego `.gitignore` para entorno virtual, sqlite y caches.

Archivos tocados:
- `.gitignore`
- `apps/anuncio/api.py`
- `apps/anuncio/models.py`
- `apps/anuncio/serializers.py`
- `apps/anuncio/url.py`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`

### PR #2 - `feature/Valentino` - merge `329848b`

Commit del branch:
- `298d60b`: `Implementacion CRUD de anuncios con APIView y asignacion forzada de publicado_por en alta de anuncio`

Cambios incorporados:
- Se extendio `apps/anuncio/api.py` con CRUD de `Anuncio` usando `APIView`.
- En el alta de anuncio, `publicado_por` se fuerza con `Usuario` id=1.
- Se ampliaron rutas en `apps/anuncio/url.py` para endpoints de anuncio.
- Se actualizo `db.sqlite3`.

Archivos tocados:
- `apps/anuncio/api.py`
- `apps/anuncio/url.py`
- `db.sqlite3`

### PR #3 - `feature/paula-valentino-pair` - merge `a2b6b17`

Commit del branch:
- `519843f`: `categorias_ids con write_only en AnuncioSerializer`

Cambios incorporados:
- Se agrego `categorias_ids` como campo `write_only` en `AnuncioSerializer`.
- La creacion y actualizacion de anuncios paso a requerir categorias existentes.
- El serializer expone `categorias` en lectura y recibe `categorias_ids` en escritura.
- Se agrego el propio `README.md` con el primer resumen del trabajo.
- Se agrego `docs/pruebas_postman.png` como evidencia visual de pruebas.

Archivos tocados:
- `README.md`
- `apps/anuncio/serializers.py`
- `docs/pruebas_postman.png`

### PR #5 - `feature/Paula-Valentino-TP3` - merge `d136e95`

Commits del branch:
- `9c0e25f`: `generic y viewset`
- `6b7217a`: `feat: agregar perform_create y accion tiempo-restante`

Cambios incorporados:
- Se sumaron generic views para categorias y anuncios.
- Se agregaron `CategoriaViewSet` y `AnuncioViewSet`.
- Se creo `subastas_clase/router.py` para registrar viewsets con `DefaultRouter`.
- Se incorporo `perform_create` para centralizar la asignacion de `publicado_por`.
- Se agrego la accion custom `tiempo-restante` en `AnuncioViewSet`.
- Se ajustaron URLs globales para exponer las nuevas rutas del router.
- Se agrego `lavarropas.jpg` y se actualizo `db.sqlite3` como recursos de prueba.

Archivos tocados:
- `apps/anuncio/api.py`
- `apps/anuncio/url.py`
- `subastas_clase/router.py`
- `subastas_clase/urls.py`
- `lavarropas.jpg`
- `db.sqlite3`

### PR #6 - `feature/Paula-Valentino-TP4` - merge `80df423`

Commits del branch:
- `300cfed`: `feat: agregar validaciones a las operaciones de anuncios`
- `1966463`: `feat: agregar filtros y orden en la consulta de categorias y anuncios, versionado por url`
- `e8f78c6`: `paginacion`
- `85ed30c`: `fix: versionado de api, filtros y orden modificados`
- `ec81478`: `fix: compatibilidad de api views con versionado por url`

Cambios incorporados:
- Se agregaron validaciones sobre operaciones de anuncios.
- Se incorporaron filtros y orden para consultas de categorias y anuncios.
- Se agrego versionado de la API por URL.
- Se sumo paginacion.
- Se adapto la compatibilidad de las APIViews con el esquema de versionado.
- Se creo `apps/anuncio/filters.py`.
- Se creo `apps/anuncio/v1_urls.py`.
- Se ajustaron serializers, settings, modelos y URLs globales para soportar esos cambios.
- Se agregaron `analisis_commits_tp4.pdf` y `bici de montaña.jpg` como archivos asociados a esa entrega.

Archivos tocados:
- `apps/anuncio/api.py`
- `apps/anuncio/filters.py`
- `apps/anuncio/models.py`
- `apps/anuncio/serializers.py`
- `apps/anuncio/v1_urls.py`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`
- `db.sqlite3`
- `analisis_commits_tp4.pdf`
- `bici de montaña.jpg`

## Estado funcional resumido

Segun el historial revisado, el proyecto fue incorporando estas capas de API:

- CRUD de `Categoria` con `APIView`.
- CRUD de `Anuncio` con `APIView`.
- Generic views para categorias y anuncios.
- Viewsets para categorias y anuncios.
- Accion custom `tiempo-restante` para anuncios.
- Validaciones, filtros, orden, paginacion y versionado por URL en la evolucion posterior del repositorio.

## Evidencia manual

![Endpoints probados en Postman](docs/pruebas_postman.png)

## Referencias de pull requests

- PR #1: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/1>
- PR #2: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/2>
- PR #3: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/3>
- PR #5: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/5>
- PR #6: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/6>
