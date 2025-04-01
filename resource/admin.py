from django.contrib import admin
from .models import EducationalResource

@admin.register(EducationalResource)
class EducationalResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'resource_type')  # Updated fields
    list_filter = ('resource_type', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')