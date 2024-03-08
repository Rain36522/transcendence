from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active']
    # Supposons que list_filter et search_fields restent inchangés
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
		(None, {'fields': ('nombre_victoires', 'nombre_defaites', 'historique_resultats',)}),
        # Ajoute d'autres fieldsets selon tes besoins
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
		(None, {'fields': ('nombre_victoires', 'nombre_defaites', 'historique_resultats',)}),
    )
    search_fields = ['email', 'username']
    ordering = ['email']

admin.site.register(CustomUser, CustomUserAdmin)
