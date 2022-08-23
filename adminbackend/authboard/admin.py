from django.contrib import admin
from .models import User
from typing import List, Sequence

# Register your models here.
@admin.register(User)
class AdminUserInformation(admin.ModelAdmin):
    list_display: List[str] = ["email", "name", "created_at"]
    list_display_links: List[str] = ["email"]
    search_fields: Sequence[str] = ["created_at"]
    
    def email_length(self, User: User):
        return len(self.email)
    email_length.short_description = "이메일 길이"