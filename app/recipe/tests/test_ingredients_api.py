from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """ Test publicly available ingredeints API """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """ Test login is reqd to access the API """

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """ Test Ingredients can be retrieved by authorized user """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@rsas.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """ test retrieving a list of ingredients """

        Ingredient.objects.create(user=self.user, name='Cucumber')
        Ingredient.objects.create(user=self.user, name='Banana')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """ Test that ingredients of authenticated users are returned """
        user_2 = get_user_model().objects.create_user(
            'testraj@rajic.vom',
            'testpasswe'
        )
        Ingredient.objects.create(user=user_2, name='Orange')
        ingredient = Ingredient.objects.create(user=self.user, name='Turmeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """ Test create a new ingredient """

        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(user=self.user,
                                           name=payload['name']).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """ Test creating Invalid ingredient failed """

        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
