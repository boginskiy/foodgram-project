import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipes.models import (
    FavoriteRecipe, Ingredient, IngredientRecipe,
    Recipe, ShoppingList, Tag)
from ..users.serializers import UserMultiSerializer


class IngredientListDetailSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки поля ингредиенты в рецепте."""

    id = serializers.IntegerField(required=True, source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True, source='ingredient.measurement_unit')
    amount = serializers.FloatField(required=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(serializers.ImageField):
    """Преобразование поля Image. Файл принимается в
    кодировке base64 и декодируется. далее изображение сохраняется в базе.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов на чтение."""

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации модели Recipe."""

    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.ListField(write_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('tags', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')

    def to_representation(self, instance):
        """Переопределение сериализатора для операции чтения."""

        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data

    def tags_create_update_func(self, arr_list, obj_recipe):
        """Функция записи поля tags модели Recipe."""

        if obj_recipe.tags:
            obj_recipe.tags.clear()

        for tag in arr_list:
            tag_recipe = get_object_or_404(Tag, id=tag)
            obj_recipe.tags.add(tag_recipe)
        return obj_recipe

    def ingredients_create_update_func(self, arr_dict, obj_recipe):
        """Функция записи поля ingredients модели Recipe."""

        if obj_recipe.ingredients:
            obj_recipe.ingredients.clear()

        for ingredient in arr_dict:
            id = ingredient['ingredient']['id']
            amount = ingredient['amount']

            ingred_recipe, status = IngredientRecipe.objects.get_or_create(
                ingredient_id=id, amount=amount)
            obj_recipe.ingredients.add(ingred_recipe)
        return obj_recipe

    def create(self, validated_data):
        """Кастомный метод создания рецептов."""

        ingredients_dict = validated_data.pop('ingredients')
        tags_list = validated_data.pop('tags')
        new_recipe = Recipe.objects.create(**validated_data)

        self.ingredients_create_update_func(ingredients_dict, new_recipe)

        self.tags_create_update_func(tags_list, new_recipe)
        return new_recipe

    def update(self, instance, validated_data):
        """Кастомный метод обновления рецептов."""

        new_ingredients = validated_data.pop('ingredients')
        new_tags = validated_data.pop('tags')

        self.ingredients_create_update_func(new_ingredients, instance)

        self.tags_create_update_func(new_tags, instance)
        return super().update(instance, validated_data)


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации модели Recipe."""

    author = UserMultiSerializer(default=serializers.CurrentUserDefault())
    ingredients = IngredientRecipeSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """Определяет фавориты рецептов."""

        current_user = self.context['request'].user

        if current_user.is_authenticated:
            queryset = FavoriteRecipe.objects.filter(
                user=current_user, recipe=obj).exists()
            return queryset
        return False

    def get_is_in_shopping_cart(self, obj):
        """Определяет рецепты в шоп листе."""

        current_user = self.context['request'].user
        if current_user.is_authenticated:
            queryset = ShoppingList.objects.filter(
                user=current_user, recipe=obj).exists()
            return queryset
        return False

    def validate_cooking_time(self, value):
        """Валидация времени приготовления блюда."""

        if value <= 0:
            raise serializers.ValidationError(
                'Время приготовления от 1 мин.')
        return value

    class Meta:
        model = Recipe
        fields = '__all__'
