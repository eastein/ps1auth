from django.contrib import admin
from .models import PS1Group

@admin.register(PS1Group)
class AuthorAdmin(admin.ModelAdmin):
    pass
