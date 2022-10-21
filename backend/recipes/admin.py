from django.contrib import admin
from .models import (
    Recipe, Ingredient, Tag, IngredientRecipe,
    TagRecipe, FavoriteRecipe, ShoppingList)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'image', 'text', 'cooking_time')
    list_filter = ()


admin.site.register(Recipe, RecipeAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ()


admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ()


admin.site.register(Ingredient, IngredientAdmin)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    list_filter = ()


admin.site.register(IngredientRecipe, IngredientRecipeAdmin)


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'recipe')
    list_filter = ()


admin.site.register(TagRecipe, TagRecipeAdmin)


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ()


admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ()


admin.site.register(ShoppingList, ShoppingListAdmin)
