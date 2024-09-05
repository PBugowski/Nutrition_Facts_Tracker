from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class EditionDate(models.Model):
    edition_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class NutritionFacts(models.Model):
    product_name = models.CharField(max_length=100, unique=True, verbose_name='Nazwa produktu:')
    energy_value = models.SmallIntegerField(verbose_name='Wartość energetyczna:', blank=True)
    proteins = models.SmallIntegerField(verbose_name='Białko:', blank=True)
    total_fats = models.SmallIntegerField(verbose_name='Tłuszcze:', blank=True)
    saturated_fats = models.SmallIntegerField(verbose_name='W tym tłuszcze nasycone:', blank=True)
    carbohydrates = models.SmallIntegerField(verbose_name='Węglowodany:', blank=True)
    sugars = models.SmallIntegerField(verbose_name='W tym cukry:', blank=True)
    cholesterol = models.SmallIntegerField(verbose_name='Cholesterol:', blank=True)
    fiber = models.SmallIntegerField(verbose_name='Błonnik:', blank=True)
    example = models.BooleanField(default=False, verbose_name='Pozycja dla tabeli wzorcowej')


class Training(models.Model):
    training_name = models.CharField(max_length=100, verbose_name='Nazwa treningu:', blank=True)
    level_of_experience = models.CharField(max_length=100, verbose_name='Stopień zaawansowania:')
    intensity = models.CharField(max_length=100, verbose_name='Intensywność:')
    kcal_burnt = models.SmallIntegerField(verbose_name='Spalone kalorie:', blank=True)
    trained_part = models.CharField(verbose_name='Trenowana partia mięśni:')
    exercise_1 = models.CharField(max_length=100, verbose_name='Ćwiczenie 1:', blank=True)
    exercise_1_sets = models.SmallIntegerField(verbose_name='Ilość serii:', blank=True)
    exercise_1_reps = models.SmallIntegerField(verbose_name='Ilość powtórzeń', blank=True)
    exercise_1_description = models.TextField(verbose_name='Opis ćwiczenia 1:', blank=True)
    exercise_2 = models.CharField(max_length=100, verbose_name='Ćwiczenie 2:', blank=True)
    exercise_2_sets = models.SmallIntegerField(verbose_name='Ilość serii:', blank=True)
    exercise_2_reps = models.SmallIntegerField(verbose_name='Ilość powtórzeń', blank=True)
    exercise_2_description = models.TextField(verbose_name='Opis ćwiczenia 2:', blank=True)
    exercise_3 = models.CharField(max_length=100, verbose_name='Ćwiczenie 3:', blank=True)
    exercise_3_sets = models.SmallIntegerField(verbose_name='Ilość serii:', blank=True)
    exercise_3_reps = models.SmallIntegerField(verbose_name='Ilość powtórzeń', blank=True)
    exercise_3_description = models.TextField(verbose_name='Opis ćwiczenia 3:', blank=True)
    exercise_4 = models.CharField(max_length=100, verbose_name='Ćwiczenie 4:', blank=True)
    exercise_4_sets = models.SmallIntegerField(verbose_name='Ilość serii:', blank=True)
    exercise_4_reps = models.SmallIntegerField(verbose_name='Ilość powtórzeń', blank=True)
    exercise_4_description = models.TextField(verbose_name='Opis ćwiczenia 4:', blank=True)
    exercise_5 = models.CharField(max_length=100, verbose_name='Ćwiczenie 5:', blank=True)
    exercise_5_sets = models.SmallIntegerField(verbose_name='Ilość serii:', blank=True)
    exercise_5_reps = models.SmallIntegerField(verbose_name='Ilość powtórzeń', blank=True)
    exercise_5_description = models.TextField(verbose_name='Opis ćwiczenia 5:', blank=True)
