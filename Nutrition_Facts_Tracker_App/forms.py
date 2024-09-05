from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

from Nutrition_Facts_Tracker_App.models import NutritionFacts, Training

User = get_user_model()


class RegisterUserForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika", required=True)
    email = forms.EmailField(label="Adres email", required=True)
    first_name = forms.CharField(label="Imię", max_length=100, required=False)
    last_name = forms.CharField(label="Nazwisko", max_length=100, required=False)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput, required=True)
    repeat_password = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput, required=True)

    def clean_username(self):
        cd = super().clean()
        username = cd.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Użytkownik o podanej nazwie już istnieje!')
        else:
            return username

    def clean(self):
        cd = super().clean()
        password = cd.get('password')
        repeat = cd.get('repeat_password')
        if password != repeat:
            self.add_error('repeat_password', 'Hasła nie mogą być różne!')

    def clean_email(self):
        cd = super().clean()
        email = cd.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Użytkownik o podanym adresie email już istnieje!')
        else:
            return email


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Niepoprawny login lub hasło!")
        else:
            self.user = user


class EditProfileForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    email = forms.EmailField(label="Adres email")
    first_name = forms.CharField(label="Imię")
    last_name = forms.CharField(label="Nazwisko")
    password = forms.CharField(label="Stare hasło", widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput, required=False)
    repeat_new_password = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput, required=False)


class AddNutritionFactsForUserForm(forms.ModelForm):
    class Meta:
        model = NutritionFacts
        fields = ['product_name', 'energy_value', 'proteins', 'total_fats', 'saturated_fats',
                  'carbohydrates', 'sugars', 'cholesterol', 'fiber', 'example']
        widgets = {
            'energy_value': forms.HiddenInput,
            'proteins': forms.HiddenInput,
            'total_fats': forms.HiddenInput,
            'saturated_fats': forms.HiddenInput,
            'carbohydrates': forms.HiddenInput,
            'sugars': forms.HiddenInput,
            'cholesterol': forms.HiddenInput,
            'fiber': forms.HiddenInput,
            'example': forms.HiddenInput
        }


class AddNutritionFactsForSuperuserForm(AddNutritionFactsForUserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['example'].widget = forms.CheckboxInput()


class AddTrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['training_name', 'level_of_experience', 'intensity', 'kcal_burnt', 'trained_part',
                  'exercise_1', 'exercise_2', 'exercise_3', 'exercise_4', 'exercise_5', 'exercise_1_reps',
                  'exercise_2_reps', 'exercise_3_reps', 'exercise_4_reps', 'exercise_5_reps',
                  'exercise_1_sets', 'exercise_2_sets', 'exercise_3_sets', 'exercise_4_sets',
                  'exercise_5_sets', 'exercise_1_description', 'exercise_2_description',
                  'exercise_3_description', 'exercise_4_description', 'exercise_5_description']
        LEVEL_CHOICES = (
            ('Początkujący', 'Początkujący'),
            ('Średnio zaawansowany', 'Średnio zaawansowany'),
            ('Zaawansowany', 'Zaawansowany'),
        )
        INTENSITY_CHOICES = (
            ('Spokojny', 'Spokojny'),
            ('Zrównoważony', 'Zrównoważony'),
            ('Intensywny', 'Intensywny'),
        )
        widgets = {
            'training_name': forms.HiddenInput,
            'level_of_experience': forms.Select(choices=LEVEL_CHOICES, attrs={'class': 'form-control'}),
            'intensity': forms.Select(choices=INTENSITY_CHOICES, attrs={'class': 'form-control'}),
            'kcal_burnt': forms.HiddenInput,
            'exercise_1': forms.HiddenInput,
            'exercise_2': forms.HiddenInput,
            'exercise_3': forms.HiddenInput,
            'exercise_4': forms.HiddenInput,
            'exercise_5': forms.HiddenInput,
            'exercise_1_reps': forms.HiddenInput,
            'exercise_2_reps': forms.HiddenInput,
            'exercise_3_reps': forms.HiddenInput,
            'exercise_4_reps': forms.HiddenInput,
            'exercise_5_reps': forms.HiddenInput,
            'exercise_1_sets': forms.HiddenInput,
            'exercise_2_sets': forms.HiddenInput,
            'exercise_3_sets': forms.HiddenInput,
            'exercise_4_sets': forms.HiddenInput,
            'exercise_5_sets': forms.HiddenInput,
            'exercise_1_description': forms.HiddenInput,
            'exercise_2_description': forms.HiddenInput,
            'exercise_3_description': forms.HiddenInput,
            'exercise_4_description': forms.HiddenInput,
            'exercise_5_description': forms.HiddenInput,
        }
