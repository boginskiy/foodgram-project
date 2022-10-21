import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from recipes.models import (
    FavoriteRecipe, Ingredient, IngredientRecipe,
    Recipe, ShoppingList, Tag, TagRecipe)
from ..users.serializers import UserMultiSerializer

# ----- Tag -----


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)

# ----- Ingredient -----


class IngredientListDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

# ----- Recipes-ingredient -----


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True, source='ingredient.measurement_unit')
    amount = serializers.IntegerField(required=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

# ----- Recipes-tag -----


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source='tag.id')
    name = serializers.CharField(read_only=True, source='tag.name')
    color = serializers.CharField(read_only=True, source='tag.color')
    slug = serializers.CharField(read_only=True, source='tag.slug')

    class Meta:
        model = TagRecipe
        fields = ('id', 'name', 'color', 'slug')

# ----- Recipes-image -----


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

# ----- Recipes -----


class RecipeSerializer(serializers.ModelSerializer):
    author = UserMultiSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, source='ingred_rec')
    tags = TagSerializer(read_only=True, many=True, source='tag_rec')
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        queryset = FavoriteRecipe.objects.filter(
            user=current_user, recipe=obj).exists()
        return queryset

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user
        queryset = ShoppingList.objects.filter(
            user=current_user, recipe=obj).exists()
        return queryset

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Время приготовления от 1 мин.')
        return value

    def validate(self, data):
        current_user = self.context['request'].user

        if self.context['request'].method == 'POST':
            name_recipe = self.context['request'].data['name']
            if Recipe.objects.filter(
                    name=name_recipe, author=current_user).exists():
                raise serializers.ValidationError(
                    'Не более одного рецепта с одинаковым названием')
            return data

        if self.context['request'].method == 'PATCH':
            admin = self.context['request'].user.is_staff
            author = self.instance.author
            if current_user != author and not admin:
                raise serializers.ValidationError(
                    'Вы не можете изменять чужой контент')
            return data
        return data

    def create(self, validated_data):
        ingredients_dict = validated_data.pop('ingred_rec')  # ?
        name_recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_dict:
            id_ = ingredient['id']
            amount_ = ingredient['amount']

            name_ingredient = Ingredient.objects.get(id=id_)
            IngredientRecipe.objects.create(
                ingredient=name_ingredient, recipe=name_recipe,
                amount=amount_)

        tags_list = self.context.get('tags')
        for tag_id in tags_list:
            tag_ = Tag.objects.get(id=tag_id)
            TagRecipe.objects.create(tag=tag_, recipe=name_recipe)

        return name_recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)

        if 'ingred_rec' in validated_data:
            all_current_ingredients = instance.ingred_rec.all()
            for current_ingredient in all_current_ingredients:
                current_ingredient.delete()

            new_ingredients = validated_data.pop('ingred_rec')
            for new_ingredient in new_ingredients:
                id_ = new_ingredient['id']
                amount_ = new_ingredient['amount']
                name_ingredient = Ingredient.objects.get(id=id_)
                IngredientRecipe.objects.create(
                    ingredient=name_ingredient, recipe=instance,
                    amount=amount_)

        new_tags_list = self.context.get('tags')
        if new_tags_list:
            all_current_tags = instance.tag_rec.all()
            for current_tag in all_current_tags:
                current_tag.delete()

            for tag_id in new_tags_list:
                tag_ = Tag.objects.get(id=tag_id)
                TagRecipe.objects.create(tag=tag_, recipe=instance)

        instance.save()
        return instance
