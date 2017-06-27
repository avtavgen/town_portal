from django.contrib import admin
from .models import Post, Suka


@admin.register(Post)
class PosterAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Suka)
class SukaAdmin(admin.ModelAdmin):
    list_display = ('name', 'body')
    prepopulated_fields = {'slug': ('name',)}
