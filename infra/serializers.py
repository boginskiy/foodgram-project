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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки поля ингредиенты в рецепте."""

    id = serializers.IntegerField(required=True)
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True, source='ingredient.measurement_unit')
    amount = serializers.FloatField(required=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    id = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор базовый для модели Recipe."""

    author = UserMultiSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

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

    def create(self, validated_data):
        """Кастомный метод создания рецептов."""

        ingredients_dict = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_dict:
            id_ = ingredient['id']
            amount_ = ingredient['amount']

            ing_rec, status = IngredientRecipe.objects.get_or_create(
                ingredient_id=id_, amount=amount_)
            new_recipe.ingredients.add(ing_rec)

        tags_list = self.context.get('tags')
        for tag_id in tags_list:
            tag_rec = get_object_or_404(Tag, id=tag_id)
            new_recipe.tags.add(tag_rec)

        return new_recipe

    def update(self, instance, validated_data):
        """Кастомный метод обновления рецептов."""

        new_ingred = validated_data.pop('ingredients')
        current_ingred = instance.ingredients.all()

        if new_ingred:

            # clean recipes ing
            for obj in current_ingred:
                obj.recipe_set.remove(instance)

            for new_ing in new_ingred:
                update_rec, status = IngredientRecipe.objects.get_or_create(
                ingredient_id=new_ing['id'], amount=new_ing['amount'])
                instance.ingredients.add(update_rec)
        else:
            for cur_ing in current_ingred:
                instance.ingredients.add(cur_ing)

            for cur_ing in current_ingred:
                update_rec, status = IngredientRecipe.objects.get_or_create(
                ingredient_id=cur_ing.ingredient.id, amount=cur_ing.amount)
                instance.ingredients.add(cur_ing)

        # if new_ingred == []:
        #     for cur_ing in current_ingred:
        #         instance.ingredients.add(cur_ing.id)

        # elif new_ingred:
        #     for new_ing in new_ingred:
        #         update_rec, status = IngredientRecipe.objects.get_or_create(
        #         ingredient_id=new_ing['id'], amount=new_ing['amount'])
        #         instance.ingredients.add(update_rec.id) # Тут получим id лиюо новых пар либо старых

# --------------
# cur_ing.id
        # for щио in current_ingred:
        #     instance.ingredients.remove(cur_ing.id)

        # if new_ingred:
        #     for new_ing in new_ingred:
        #         update_rec, status = IngredientRecipe.objects.get_or_create(
        #         ingredient_id=new_ing['id'], amount=new_ing['amount'])
        #         instance.ingredients.add(update_rec)
        # else:
        #     for cur_ing in current_ingred:
        #         update_rec, status = IngredientRecipe.objects.get_or_create(
        #         ingredient_id=cur_ing.ingredient.id, amount=cur_ing.amount)
        #         instance.ingredients.add(cur_ing)

# ---------------------------------------------------------------
        new_tags_list = self.context.get('tags')
        all_tags_recipe = instance.tags.all()

        if new_tags_list:
            for tag_rec in all_tags_recipe:
                instance.tags.remove(tag_rec.id)

            for tag_id in new_tags_list:
                tag_rec = get_object_or_404(Tag, id=tag_id)
                instance.tags.add(tag_rec)

        super().update(instance, validated_data)
        return instance
