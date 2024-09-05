import pytest

from django.contrib.auth import get_user_model

from Nutrition_Facts_Tracker_App.models import NutritionFacts, Training

User = get_user_model()


@pytest.fixture
def create_users():
    superuser = {
        'password': 'superuser',
        'last_login': '2024-07-08 10:59:45.859541 +00:00',
        'is_superuser': True,
        'username': 'superuser',
        'first_name': 'superuser',
        'last_name': 'superuser',
        'email': 'superuser@superuser.com',
        'is_staff': True,
        'is_active': True,
        'date_joined': '2024-07-01 14:14:39.301207 +00:00',
    }
    user = {
        'password': 'user',
        'last_login': '2024-07-08 10:59:45.859541 +00:00',
        'is_superuser': True,
        'username': 'user',
        'first_name': 'user',
        'last_name': 'user',
        'email': 'user@user.com',
        'is_staff': True,
        'is_active': True,
        'date_joined': '2024-07-01 14:14:39.301207 +00:00',
    }
    User.objects.create_user(**user)
    User.objects.create_user(**superuser)


@pytest.fixture
def create_login(client):
    User.objects.create_user(
        password='superuser',
        last_login='2024-07-08 10:59:45.859541 +00:00',
        is_superuser=True,
        username='superuser',
        first_name='superuser',
        last_name='superuser',
        email='superuser@superuser.com',
        is_staff=True,
        is_active=True,
        date_joined='2024-07-01 14:14:39.301207 +00:00'
    )
    client.login(username='superuser', password='superuser')


@pytest.fixture
def create_trainings():
    training_1 = {
        'training_name': 'Spokojny - Zaawansowany - fake part',
        'level_of_experience': 'Zaawansowany',
        'intensity': 'Spokojny',
        'kcal_burnt': '11',
        'trained_part': 'fake part',
        'exercise_1': 'fake exercise 1',
        'exercise_2': 'fake exercise 2',
        'exercise_3': 'fake exercise 3',
        'exercise_4': 'fake exercise 4',
        'exercise_5': 'fake exercise 5',
        'exercise_1_reps': '1',
        'exercise_2_reps': '2',
        'exercise_3_reps': '3',
        'exercise_4_reps': '4',
        'exercise_5_reps': '5',
        'exercise_1_sets': '6',
        'exercise_2_sets': '7',
        'exercise_3_sets': '8',
        'exercise_4_sets': '9',
        'exercise_5_sets': '10',
        'exercise_1_description': 'fake exercise 1 description',
        'exercise_2_description': 'fake exercise 2 description',
        'exercise_3_description': 'fake exercise 3 description',
        'exercise_4_description': 'fake exercise 4 description',
        'exercise_5_description': 'fake exercise 5 description',
    }
    training_2 = {
        'training_name': 'Intensywny - Średnio zaawansowany - fake part 2',
        'level_of_experience': 'Średnio zaawansowany',
        'intensity': 'Intensywny',
        'kcal_burnt': '1111',
        'trained_part': 'fake part 2',
        'exercise_1': 'fake exercise 11',
        'exercise_2': 'fake exercise 22',
        'exercise_3': 'fake exercise 33',
        'exercise_4': 'fake exercise 44',
        'exercise_5': 'fake exercise 55',
        'exercise_1_reps': '11',
        'exercise_2_reps': '22',
        'exercise_3_reps': '33',
        'exercise_4_reps': '44',
        'exercise_5_reps': '55',
        'exercise_1_sets': '66',
        'exercise_2_sets': '77',
        'exercise_3_sets': '88',
        'exercise_4_sets': '99',
        'exercise_5_sets': '1010',
        'exercise_1_description': 'fake exercise 11 description',
        'exercise_2_description': 'fake exercise 22 description',
        'exercise_3_description': 'fake exercise 33 description',
        'exercise_4_description': 'fake exercise 44 description',
        'exercise_5_description': 'fake exercise 55 description',
    }
    Training.objects.create(**training_1)
    Training.objects.create(**training_2)


@pytest.fixture
def create_products():
    product_1 = {
        'id': 1,
        'product_name': 'fake product',
        'energy_value': '1',
        'proteins': '2',
        'total_fats': '3',
        'saturated_fats': '4',
        'carbohydrates': '5',
        'sugars': '6',
        'cholesterol': '7',
        'fiber': '8',
        'example': True
    }
    product_2 = {
        'id': 2,
        'product_name': 'fake product 2',
        'energy_value': '11',
        'proteins': '22',
        'total_fats': '33',
        'saturated_fats': '44',
        'carbohydrates': '55',
        'sugars': '66',
        'cholesterol': '77',
        'fiber': '88',
        'example': False
    }
    NutritionFacts.objects.create(**product_1)
    NutritionFacts.objects.create(**product_2)
