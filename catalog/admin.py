from django.contrib import admin
from blog.models import Blog
from catalog.models import Product, Category, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'price', 'category', 'created_at',
        'updated_at', 'is_published', 'view_counter')
    readonly_fields = ('created_at', 'updated_at', 'view_counter')
    list_filter = ('category', 'is_published', 'price')
    search_fields = ('product', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'number', 'is_current', 'product')
    list_filter = ('product', 'is_current')
    search_fields = ('title', 'product')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created_at', 'updated_at', 'view_counter')
    list_filter = ('is_published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
