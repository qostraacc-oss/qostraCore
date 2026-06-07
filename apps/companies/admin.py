from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace', 'company_size', 'industry', 'created_at')
    list_filter = ('company_size', 'industry', 'created_at')
    search_fields = ('name', 'workspace__name')
