from django.urls import include, path
from .users.views import (
    users_detail, users_me, users_list_signup, users_set_password,
    users_subscriptions, users_subscribe_delete)
from .recipes.views import (
    tags_detail, tags_list,
    ingredients_detail, ingredients_list,
    recipes_detail, recipes_detail_shop_cart, recipes_favorite,
    recipes_list_create, recipes_shop_cart_download)


urlpatterns = [
    # Подписки
    path('users/subscriptions/', users_subscriptions),
    path('users/<int:users_id>/subscribe/', users_subscribe_delete),

    # Users
    path('users/set_password/', users_set_password),
    path('users/<int:users_id>/', users_detail),
    path('users/me/', users_me),
    path('users/', users_list_signup),

    # Authtoken
    path('auth/', include('djoser.urls.authtoken')),

    # Теги
    path('tags/<int:tags_id>/', tags_detail),
    path('tags/', tags_list),

    # Ингредиенты
    path('ingredients/', ingredients_list),
    path('ingredients/<int:ingredients_id>/', ingredients_detail),

    # Рецепты
    path('recipes/', recipes_list_create, name='recipes'),
    path('recipes/<int:recipes_id>/', recipes_detail, name='recipes_detail'),

    # Избранное
    path('recipes/<int:recipes_id>/favorite/', recipes_favorite),

    # Список покупок
    path('recipes/download_shopping_cart/', recipes_shop_cart_download),
    path('recipes/<int:recipes_id>/shopping_cart/', recipes_detail_shop_cart),

]
