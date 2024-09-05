import json
from unittest.mock import patch

import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from .models import NutritionFacts, Training

User = get_user_model()


@pytest.mark.django_db
def test_landing_page_view(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_user_view_pass(client):
    response = client.post(
        '/register/',
        {
            'username': 'example0',
            'email': 'example@example.com',
            'first_name': 'example1',
            'last_name': 'example2',
            'password': 'example3',
            'repeat_password': 'example3',
        }
    )
    assert response.status_code == 200
    user = User.objects.get(username='example0')
    assert user.email == 'example@example.com'
    assert user.first_name == 'example1'
    assert user.last_name == 'example2'
    assert check_password('example3', user.password)


@pytest.mark.django_db
def test_register_user_view_fail_username(client, create_users):
    response = client.post(
        '/register/',
        {
            'username': 'user',
            'email': 'example@example.com',
            'first_name': 'example1',
            'last_name': 'example2',
            'password': 'example3',
            'repeat_password': 'example3',
        }
    )
    assert 'username' in response.context['form'].errors
    assert User.objects.count() == 2


@pytest.mark.django_db
def test_register_user_view_fail_email(client, create_users):
    response = client.post(
        '/register/',
        {
            'username': 'example0',
            'email': 'superuser@superuser.com',
            'first_name': 'example1',
            'last_name': 'example2',
            'password': 'example3',
            'repeat_password': 'example3',
        }
    )
    assert 'email' in response.context['form'].errors
    assert User.objects.count() == 2


@pytest.mark.django_db
def test_register_user_view_fail_password(client, create_users):
    response = client.post(
        '/register/',
        {
            'username': 'example0',
            'email': 'example@example.com',
            'first_name': 'example1',
            'last_name': 'example2',
            'password': 'example3',
            'repeat_password': 'example4',
        }
    )
    assert 'repeat_password' in response.context['form'].errors
    assert User.objects.count() == 2


@pytest.mark.django_db
def test_login_user_view_success(client, create_users):
    response = client.post(
        '/login/',
        {
            'username': 'superuser',
            'password': 'superuser',
        }
    )
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_login_user_view_fail_username(client, create_users):
    response = client.post(
        '/login/',
        {
            'username': 'user',
            'password': 'superuser',
        }
    )
    assert response.wsgi_request.user.is_authenticated is False


@pytest.mark.django_db
def test_login_user_view_fail_password(client, create_users):
    response = client.post(
        '/login/',
        {
            'username': 'superuser',
            'password': 'user',
        }
    )
    assert response.wsgi_request.user.is_authenticated is False


@pytest.mark.django_db
def test_logout_user_view(client):
    response = client.get(
        '/logout/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_view_for_logged_in_user(client, create_login):
    response = client.get(
        '/dashboard/'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard_view_for_logged_out_user(client):
    response = client.get(
        '/dashboard/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_profile_view_for_logged_in_user(client, create_login):
    response = client.get(
        '/profile/'
    )
    assert response.status_code == 200
    assert response.context['username'] == 'superuser'
    assert response.context['email'] == 'superuser@superuser.com'
    assert response.context['first_name'] == 'superuser'
    assert response.context['last_name'] == 'superuser'


@pytest.mark.django_db
def test_get_profile_view_for_logged_out_user(client):
    response = client.get(
        '/profile/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_profile_view_for_logged_in_user(client, create_login):
    response = client.get(
        '/edit_profile/'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_edit_profile_view_for_logged_out_user(client):
    response = client.get(
        '/edit_profile/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_add_nutrition_facts_view_for_logged_in_user(client, create_login):
    response = client.get(
        '/add_product/'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_add_nutrition_facts_view_for_logged_out_user(client):
    response = client.get(
        '/add_product/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_product_list_view_for_logged_in_user(client, create_login, create_products):
    response = client.get(
        '/products/'
    )
    assert response.status_code == 200
    assert 'fake product' in response.content.decode()
    assert 'fake product 2' in response.content.decode()
    assert NutritionFacts.objects.count() == 2


@pytest.mark.django_db
def test_product_details_view_for_logged_in_user(client, create_login, create_products):
    response = client.get(
        '/products/1/'
    )
    assert response.status_code == 200
    assert 'fake product' in response.content.decode()
    assert '1' in response.content.decode()
    assert '2' in response.content.decode()
    assert '3' in response.content.decode()
    assert '4' in response.content.decode()
    assert '5' in response.content.decode()
    assert '6' in response.content.decode()
    assert '7' in response.content.decode()
    assert '8' in response.content.decode()


@pytest.mark.django_db
def test_get_add_training_view_for_logged_in_user(client, create_login):
    response = client.get(
        '/add_training/'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_add_training_view_for_logged_out_user(client):
    response = client.get(
        '/add_training/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_training_details_view_for_logged_in_user(client, create_login, create_trainings):
    response = client.get(
     '/trainings/1/'
    )
    assert 'Spokojny - Zaawansowany - fake part' in response.content.decode()
    assert '11' in response.content.decode()
    assert 'fake part' in response.content.decode()
    assert 'fake exercise 1' in response.content.decode()
    assert 'fake exercise 2' in response.content.decode()
    assert 'fake exercise 3' in response.content.decode()
    assert 'fake exercise 4' in response.content.decode()
    assert 'fake exercise 5' in response.content.decode()
    assert '1' in response.content.decode()
    assert '2' in response.content.decode()
    assert '3' in response.content.decode()
    assert '4' in response.content.decode()
    assert '5' in response.content.decode()
    assert '6' in response.content.decode()
    assert '7' in response.content.decode()
    assert '8' in response.content.decode()
    assert '9' in response.content.decode()
    assert '10' in response.content.decode()
    assert 'fake exercise 1 description' in response.content.decode()
    assert 'fake exercise 2 description' in response.content.decode()
    assert 'fake exercise 3 description' in response.content.decode()
    assert 'fake exercise 4 description' in response.content.decode()
    assert 'fake exercise 5 description' in response.content.decode()
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_training_details_view_for_logged_out_user(client):
    response = client.get(
        '/trainings/1/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_training_list_view_for_logged_in_user(client, create_login, create_trainings):
    response = client.get(
        '/trainings/'
    )
    assert response.status_code == 200
    assert 'Spokojny - Zaawansowany - fake part' in response.content.decode()
    assert 'Intensywny - Średnio zaawansowany - fake part 2' in response.content.decode()
    assert Training.objects.count() == 2


@pytest.mark.django_db
def test_get_training_list_view_for_logged_out_user(client):
    response = client.get(
        '/trainings/'
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_training_view_for_logged_in_user(client, create_login):

    mock_response = {
        "training_name": "Spokojny - Zaawansowany - Plecy",
        "kcal_burnt": 500,
        "exercise_1": "Martwy ciąg",
        "exercise_1_sets": 4,
        "exercise_1_reps": 8,
        "exercise_1_description": "Podstawowe ćwiczenie na plecy",
        "exercise_2": "Podciąganie na drążku",
        "exercise_2_sets": 4,
        "exercise_2_reps": 10,
        "exercise_2_description": "Klasyczne ćwiczenie na plecy",
        "exercise_3": "Wiosłowanie sztangą w opadzie",
        "exercise_3_sets": 4,
        "exercise_3_reps": 12,
        "exercise_3_description": "Ćwiczenie na rozwój mięśni grzbietu",
        "exercise_4": "Przyciąganie linki wyciągu dolnego",
        "exercise_4_sets": 4,
        "exercise_4_reps": 12,
        "exercise_4_description": "Ćwiczenie izolujące mięśnie najszersze grzbietu",
        "exercise_5": "Face pulls",
        "exercise_5_sets": 4,
        "exercise_5_reps": 15,
        "exercise_5_description": "Ćwiczenie na górną część pleców"
    }

    with patch("Nutrition_Facts_Tracker_App.views.AddTrainingView.get_training") as mock_call:
        mock_call.return_value = json.dumps(mock_response)

        response = client.post(
            '/add_training/',
            {
                'intensity': 'Spokojny',
                'trained_part': 'Plecy',
                'level_of_experience': 'Zaawansowany',
            }
        )

        assert response.status_code == 302
        assert response.url.startswith('/trainings/')
        last_training_id = Training.objects.all().order_by('pk').last().pk
        training = Training.objects.get(pk=last_training_id)
        assert training.training_name == mock_response['training_name']
        assert training.kcal_burnt == mock_response['kcal_burnt']
        assert training.exercise_1 == mock_response['exercise_1']
        assert training.exercise_1_sets == mock_response['exercise_1_sets']
        assert training.exercise_1_reps == mock_response['exercise_1_reps']
        assert training.exercise_1_description == mock_response['exercise_1_description']
        assert training.exercise_2 == mock_response['exercise_2']
        assert training.exercise_2_sets == mock_response['exercise_2_sets']
        assert training.exercise_2_reps == mock_response['exercise_2_reps']
        assert training.exercise_2_description == mock_response['exercise_2_description']
        assert training.exercise_3 == mock_response['exercise_3']
        assert training.exercise_3_sets == mock_response['exercise_3_sets']
        assert training.exercise_3_reps == mock_response['exercise_3_reps']
        assert training.exercise_3_description == mock_response['exercise_3_description']
        assert training.exercise_4 == mock_response['exercise_4']
        assert training.exercise_4_sets == mock_response['exercise_4_sets']
        assert training.exercise_4_reps == mock_response['exercise_4_reps']
        assert training.exercise_4_description == mock_response['exercise_4_description']
        assert training.exercise_5 == mock_response['exercise_5']
        assert training.exercise_5_sets == mock_response['exercise_5_sets']
        assert training.exercise_5_reps == mock_response['exercise_5_reps']
        assert training.exercise_5_description == mock_response['exercise_5_description']
