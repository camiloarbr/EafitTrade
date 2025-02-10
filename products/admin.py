from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'seller')
    list_filter = ('category', 'condition', 'available')
    search_fields = ('name', 'description', 'tags')
    date_hierarchy = 'published_at'