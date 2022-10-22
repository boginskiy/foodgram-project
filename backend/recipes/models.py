from django.db import models
from colorfield.fields import ColorField
from users.models import User

# ----- Recipes -----


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to='recipes/images/', blank=False)
    text = models.TextField(blank=False)
    ingredients = models.ManyToManyField(
        'Ingredient', through='IngredientRecipe')
    tags = models.ManyToManyField(
        'Tag', through='TagRecipe')
    cooking_time = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-id']

# ----- Ingredient -----


class Ingredient(models.Model):
    name = models.CharField(max_length=128, blank=False)
    measurement_unit = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['id']


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingred_rec')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingred_rec')
    amount = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.ingredient} {self.recipe} {self.amount}'

# ----- Tag -----


class Tag(models.Model):
    name = models.CharField(
        max_length=32, unique=True, blank=False)
    color = ColorField(
        default='#ffffff', format='hex', unique=True, blank=False)
    slug = models.SlugField(max_length=32, unique=True, blank=False)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        ordering = ['id']


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name='tag_rec')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='tag_rec')

    class Meta:
        ordering = ['-id']

# ----- Favorite -----


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_rec')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_rec')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']

# ----- ShoppingList -----


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shop_list')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shop_list')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
