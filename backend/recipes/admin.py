from django.contrib import admin
from .models import (
    Recipe, Ingredient, Tag, IngredientRecipe,
    FavoriteRecipe, ShoppingList)


# class RecipeIngredientInline(admin.TabularInline):
#     model = Recipe
#     extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка админки для рецептов."""

    # inlines = (RecipeIngredientInline,)
    list_display = (
        'id', 'name', 'author', 'image', 'text', 'cooking_time')
    list_display_links = ('name',)
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author__username', 'text', 'tags')
    save_on_top = True
    fieldsets = (
        ('Data', {
            'fields': (('image', 'text', 'cooking_time', 'tags',),)
        }),
        ('Composition', {
            'fields': (('ingredients',),)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка админки для тегов."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка админки для ингредиентов."""

    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Настройка админки ингредиентов для рецептов."""

    list_display = ('id', 'ingredient', 'amount')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Настройка админки для избранных рецептов."""

    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Настройка админки списка покупок."""

    list_display = ('id', 'user', 'recipe')
