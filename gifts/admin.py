from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    ordering = ['title']

admin.site.register(Article, ArticleAdmin)
