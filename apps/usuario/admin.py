from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'documento_identidad', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'documento_identidad')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informacion adicional', {'fields': ('documento_identidad', 'domicilio')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informacion adicional', {'fields': ('email', 'documento_identidad', 'domicilio')}),
    )
