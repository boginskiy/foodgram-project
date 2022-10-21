from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated)
from .paginations import RecipesListPagination
from recipes.models import (
    FavoriteRecipe, IngredientRecipe, Ingredient,
    Recipe, Tag, TagRecipe, ShoppingList)
from ..users.serializers import UserRecipeSerializer
from .serializers import (
    IngredientListDetailSerializer, RecipeSerializer, TagListSerializer)
from .permissions import PatchIsAuthorOrReadAll

# ----- Favorite -----


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def recipes_favorite(request, recipes_id):
    """Добавление рецепта в список избранное/ удаление из списка."""

    recipe = get_object_or_404(Recipe, id=recipes_id)
    logic = FavoriteRecipe.objects.filter(
        user=request.user, recipe=recipe).exists()

    if request.method == 'POST':
        if logic:
            return Response({"message": "Рецепт уже есть в списке избранное."},
                            status=status.HTTP_400_BAD_REQUEST)

        FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
        serializer = UserRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if logic:
        recipe_del = FavoriteRecipe.objects.get(recipe=recipes_id)
        recipe_del.delete()
        return Response(
            {"message": "Рецепт удален из списка избранное."},
            status=status.HTTP_204_NO_CONTENT)

    return Response(
        {'message': 'Рецепт отсутствует в списке избранное.'},
        status=status.HTTP_400_BAD_REQUEST)

# ----- Tag -----


@api_view(['GET'])
@permission_classes([AllowAny])
def tags_list(request):
    """Список текущих тегов."""

    tags = Tag.objects.all()
    serializer = TagListSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def tags_detail(request, tags_id):
    """Получение выбранного тега."""

    tag = get_object_or_404(Tag, id=tags_id)
    serializer = TagListSerializer(tag)
    return Response(serializer.data)

# ----- Ingredients -----


@api_view(['GET'])
@permission_classes([AllowAny])
def ingredients_list(request):
    """Список всех ингредиентов."""

    name = request.query_params.get('name')
    if name:
        ingredients = Ingredient.objects.filter(name__istartswith=name)
    else:
        ingredients = Ingredient.objects.all()
    serializer = IngredientListDetailSerializer(ingredients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def ingredients_detail(request, ingredients_id):
    """Получение ингредиента."""

    ingredient = get_object_or_404(Ingredient, id=ingredients_id)
    serializer = IngredientListDetailSerializer(ingredient)
    return Response(serializer.data)

# ----- Recipes -----


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def recipes_list_create(request):
    """Список всех рецептов. Создание нового."""

    if request.method == 'POST':
        if 'tags' not in request.data:
            return Response(
                {"tags": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST)

        tags = request.data.pop('tags')
        serializer = RecipeSerializer(
            data=request.data, context={'request': request, 'tags': tags})
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.query_params:
        recipes = []

        is_favorited = request.query_params.get('is_favorited', 0)
        is_in_shopping_cart = request.query_params.get(
            'is_in_shopping_cart', 0)
        author = request.query_params.get('author', 0)
        tags = dict(request.query_params.lists()).get('tags')

        if int(is_favorited):
            favorite_recipe_qwery = FavoriteRecipe.objects.filter(
                user=request.user)
            recipes = Recipe.objects.filter(
                favorite_rec__in=favorite_recipe_qwery)

        elif int(is_in_shopping_cart):
            shopping_list_qwery = ShoppingList.objects.filter(
                user=request.user)
            recipes = Recipe.objects.filter(shop_list__in=shopping_list_qwery)

        elif author:
            recipes = Recipe.objects.filter(author=int(author))

        elif tags:
            tags = Tag.objects.filter(slug__in=tags)
            tag_recipe_qwery = TagRecipe.objects.filter(tag__in=tags)
            recipes = Recipe.objects.filter(tag_rec__in=tag_recipe_qwery)
    else:
        recipes = Recipe.objects.all()

    paginator = RecipesListPagination()
    result_page = paginator.paginate_queryset(recipes, request)
    serializer = RecipeSerializer(
        result_page, context={'request': request}, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
@permission_classes([PatchIsAuthorOrReadAll])
def recipes_detail(request, recipes_id):
    """Получение конкретного рецепта, изменение, удаление."""

    recipe = get_object_or_404(Recipe, id=recipes_id)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    if request.method == 'DELETE':
        author = get_object_or_404(Recipe, id=recipes_id).author
        if request.user != author and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    tags = []
    if 'tags' in request.data:
        tags = request.data.pop('tags')

    serializer = RecipeSerializer(
        recipe, data=request.data, partial=True,
        context={'request': request, 'tags': tags})

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def recipes_detail_shop_cart(request, recipes_id):
    """Добавить рецепт в список покупок, удалить его."""

    recipe = get_object_or_404(Recipe, id=recipes_id)
    logic = ShoppingList.objects.filter(
        user=request.user, recipe=recipes_id).exists()

    if request.method == 'POST':
        if logic:
            return Response({"message": "Рецепт уже добавлен."},
                            status=status.HTTP_400_BAD_REQUEST)

        ShoppingList.objects.create(
            user=request.user, recipe=recipe)
        serializer = UserRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if not logic:
        return Response({"message": "Рецепт отсутствует в списке покупок."},
                        status=status.HTTP_400_BAD_REQUEST)

    recipe_in_list_del = ShoppingList.objects.get(recipe=recipes_id)
    recipe_in_list_del.delete()
    return Response(status=status.HTTP_201_CREATED)

# ----- Shopping_cart -----


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipes_shop_cart_download(request):
    """Сбор данных с рецептов для списка покупок. Список продуктов."""

    # Составил dict с ингредиенами из списка рецептов.
    set_recipes = ShoppingList.objects.filter(user=request.user)

    user_name = (f'{request.user.first_name.title()}_'
                 f'{request.user.last_name.title()}')

    recipes_id = []
    for set_recipe in set_recipes:
        recipes_id.append(set_recipe.recipe)

    set_ingredients = IngredientRecipe.objects.filter(
        recipe__in=recipes_id).order_by('ingredient')

    shop_cart = {}
    for ingredient in set_ingredients:
        key = (f'{ingredient.ingredient.name}('
               f'{ingredient.ingredient.measurement_unit})')

        if key in shop_cart:
            shop_cart[key] += ingredient.amount
        else:
            shop_cart[key] = ingredient.amount

    # Сделал список покупок txt.file с ингредиентами из списка рецептов.
    file = open('media/recipes/shop_cart/list.txt', 'w')
    file.write('Список покупок:\n')
    count = 1
    for key, value in shop_cart.items():
        line = f'{count}) {key} — {value}\n'
        count += 1
        file.write(line)

    with open('media/recipes/shop_cart/list.txt', 'r+') as file:
        response = HttpResponse(file, content_type="")
        response['Content-Disposition'] = (
            u'attachment; filename="%s-ShopList.txt"' % (user_name))
        return response
