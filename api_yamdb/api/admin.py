from django.contrib import admin

from .models import Genre, Title, Category, TitleGenre


class TitleGenreInline(admin.TabularInline):
    model = TitleGenre
    extra = 2


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'category']
    inlines = (TitleGenreInline,)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
