#!-*-coding:utf-8-*-
import json
import tempfile
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from users.models import User


class CommonTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='admin',
            password='admin',
            first_name='egor',
            last_name='letov',
        )
        cls.api_client = APIClient()
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self) -> None:
        self.api_client.force_authenticate(user=self.user, token=self.token)


class ReciepeViewTestCase(CommonTestCase):
    """Тест api рецептов."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('recipes')

    def setUp(self) -> None:
        super().setUp()

        self.amount = 22
        self.ing_salt = Ingredient.objects.create(
            name='salt',
            measurement_unit='g'
        )
        self.ing_honey = Ingredient.objects.create(
            name='honey',
            measurement_unit='g'
        )
        self.tag1 = Tag.objects.create(
            name='tag1',
            color='red',
            slug='tag1',
        )
        self.tag2 = Tag.objects.create(
            name='tag2',
            color='blue',
            slug='tag2',
        )

        self.ing_rec1 = IngredientRecipe.objects.create(
            ingredient=self.ing_salt,
            amount=10,
        )
        self.ing_rec2 = IngredientRecipe.objects.create(
            ingredient=self.ing_salt,
            amount=20,
        )
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image = Image.new('RGB', (100, 100))
        image.save(self.tmp_file.name)

        # self.api_client.force_authenticate(user=self.user, token=self.token)

    def create_recipe(self, **kw):
        data = {
            'name': 'salat',
            'text': 'text',
            'cooking_time': 4,
            'author': self.user,
        }
        data.update(kw)

        recipe = Recipe.objects.create(**data)

        recipe.tags.add(self.tag1)
        recipe.ingredients.add(
            self.ing_rec1
        )
        return recipe

    def test_patch_recipe(self):
        """Тест создания рецепта.
        """
        recipe = self.create_recipe()
        new_name = 'new'
        url = reverse('recipes_detail', kwargs={'recipes_id': recipe.id})

        data = {
            "name": new_name,
            "ingredients": [
                {
                    "id": self.ing_honey.id,
                    "amount": 30,
                },
            ],
        }

        resp = self.api_client.patch(path=url,
                                     data=json.dumps(data),
                                     content_type='application/json',
                                     )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        # recipe = Recipe.objects.last()
        self.assertEqual(resp.data.get('id'), recipe.id)
        self.assertEqual(resp.data.get('name'), new_name)
        print(resp.data.get('ingredients'))
        # print(recipe.ingredients)
        # self.assertEqual(recipe.ingredients.last().id, self.ing_salt.id)

    def test_list(self):
        recipe = self.create_recipe()

        resp = self.api_client.get(self.url)

        resp_data = resp.json()['results'][0]
        self.assertEqual(resp_data['name'], recipe.name)

        ing_data = resp_data['ingredients'][0]
        self.assertEqual(ing_data['id'], recipe.ingredients.last().id)
        self.assertEqual(ing_data['amount'], self.amount)
        print(resp.json())

    # Димон, тестирование view-функций
    def test_recipes_detail(self):
        receipe = self.create_recipe()
        url = reverse('api:recipes_detail', kwargs={'recipes_id': receipe.pk})
        client = Client()
        client.force_login(user=self.user)

        resp = client.get(url)

        print(resp)
        print(resp.json())

        self.assertTrue(True)
