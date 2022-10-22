from django.contrib import admin
from .models import (
    Recipe, Ingredient, Tag, IngredientRecipe,
    TagRecipe, FavoriteRecipe, ShoppingList)


class IngredientRecipeInLine(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'image', 'text', 'cooking_time')
    list_display_links = ('name',)
    list_filter = ('name', 'author', 'tags__name')
    search_fields = ('name', 'author__username', 'text', 'tags__name')

    inlines = [IngredientRecipeInLine]
    save_on_top = True
    fieldsets = (
        ('Data', {
            'fields': (('image', 'text', 'cooking_time'),)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'recipe')
    list_filter = ('tag',)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
