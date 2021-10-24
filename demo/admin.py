from django.contrib import admin

from .models import FileModel


@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
    pass
