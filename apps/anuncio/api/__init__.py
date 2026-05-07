"""
API package for anuncio.

Avoid importing DRF view classes at package import time; DRF may import
settings (and thus this package path) while it is still initializing.
"""

__all__: list[str] = []
