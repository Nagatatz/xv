from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at', 'deleted_at')


class BaseTabularInline(admin.TabularInline):
    exclude = ('created_at', 'updated_at', 'deleted_at')
