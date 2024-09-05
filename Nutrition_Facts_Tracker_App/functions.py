from openai import OpenAI

from django.contrib import messages

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model, login, authenticate

from .models import EditionDate

User = get_user_model()
client = OpenAI(
    api_key='abc123'  # Enter your api key here
)


def get_user_data(request):
    try:
        last_edition_date = EditionDate.objects.filter(user=request.user).order_by('pk').last().edition_date
    except AttributeError:
        last_edition_date = None
    ctx = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'last_edition_date': last_edition_date,
    }
    return ctx


def get_initial_user_data(request):
    ctx = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    return ctx


def verify_edited_user_data(request, data):
    errors = 0
    data['current_user'].first_name = data['first_name']
    data['current_user'].last_name = data['last_name']
    if data['current_user'].username != data['username'] and User.objects.filter(username=data['username']).exists():
        messages.error(request, 'Użytkownik o podanej nazwie już istnieje!')
        errors += 1
    else:
        data['current_user'].username = data['username']
    if data['current_user'].email != data['email'] and User.objects.filter(email=data['email']).exists():
        messages.error(request, 'Użytkownik o podanym adresie email już istnieje!')
        errors += 1
    else:
        data['current_user'].email = data['email']
    if data['password'] or data['new_password'] or data['repeat_new_password']:
        if not check_password(data['password'], data['current_user'].password):
            messages.error(request, 'Niepoprawne stare hasło!')
            errors += 1
        elif data['new_password'] != data['repeat_new_password']:
            messages.error(request, 'Nowe hasła nie mogą być różne!')
            errors += 1
        else:
            data['current_user'].set_password(data['new_password'])
    if errors == 0:
        messages.success(request, 'Zmiany zostały zapisane!')
        return True
    else:
        return False


def authenticate_and_login_edited_user(request, data):
    if data['password'] and data['new_password'] and data['repeat_new_password']:
        authenticate(username=data['current_user'].username, password=data['new_password'])
        login(request, data['current_user'])
    else:
        login(request, data['current_user'])
