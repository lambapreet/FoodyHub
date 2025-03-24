from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ('-date_joined',)  # ✅ Fixed missing comma
    search_fields = ('email', 'username', 'phone_number')  # ✅ Added search fields
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')  # ✅ Added filters

    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'username', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'create_date', 'modified_date')}),
    )

    add_fieldsets = (
        ('New User', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username', 'phone_number', 'role', 'password1', 'password2')
        }),
    )

admin.site.register(User, CustomUserAdmin)
