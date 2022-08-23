from django.contrib import admin
from .models import User
from typing import List, Sequence

# Register your models here.
@admin.register(User)
class AdminUserInformation(admin.ModelAdmin):
    list_display: List[str] = ["email", "name", 'birth_day', "created_at", "updated_at"]
    list_display_links: List[str] = ["email"]
    search_fields: Sequence[str] = ["name"]

