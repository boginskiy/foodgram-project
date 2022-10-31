from django.db import models
from colorfield.fields import ColorField
from users.models import User


class Recipe(models.Model):
    """Модель Рецептов."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to='recipes/images/', blank=False)
    text = models.TextField(blank=False)
    ingredients = models.ManyToManyField(
        'IngredientRecipe', related_name='recipe')
    tags = models.ManyToManyField('Tag', related_name='recipe')
    cooking_time = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return self.name

    def get_nominations(self):
        ingredients_list = self.ingredients.get_query_set()
        ingredients_str = ''
        for ingredient in ingredients_list:
            ingredients_str += ', ' + ingredient.title
        return ingredients_str.lstrip(', ')

    get_nominations.short_description = 'Ingredients'

    class Meta:
        ordering = ['-id']


class Ingredient(models.Model):
    """Модель Ингредиентов."""

    name = models.CharField(max_length=128, blank=False)
    measurement_unit = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['id']


class IngredientRecipe(models.Model):
    """Модель ингредиентов-рецептов."""

    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingred_rec')
    amount = models.FloatField(blank=False)

    def __str__(self):
        return f'{self.ingredient}'


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=32, unique=True, blank=False)
    color = ColorField(
        default='#ffffff', format='hex', unique=True, blank=False)
    slug = models.SlugField(max_length=32, unique=True, blank=False)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        ordering = ['id']


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_rec')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_rec')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']


class ShoppingList(models.Model):
    """Модель списков с рецептами."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shop_list')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shop_list')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
