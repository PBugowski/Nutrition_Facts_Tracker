import json

from openai import OpenAI

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import (
    AddNutritionFactsForSuperuserForm,
    AddNutritionFactsForUserForm,
    AddTrainingForm,
    EditProfileForm,
    LoginUserForm,
    RegisterUserForm,
)
from .functions import (
    authenticate_and_login_edited_user,
    get_initial_user_data,
    get_user_data,
    verify_edited_user_data,
)
from .models import (
    EditionDate,
    NutritionFacts,
    Training,
)
from .prompts import (
    generate_prompt_nutrition,
    generate_prompt_training
)

User = get_user_model()
client = OpenAI(
    api_key='abc123'  # Enter your api key here
)


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing_page.html')


class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        context = {'form': form}
        return render(request, "registration.html", context)

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            del cd['repeat_password']
            User.objects.create_user(**form.cleaned_data)
        return render(request, "registration.html", ctx)


class LoginUserView(FormView):
    form_class = LoginUserForm
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form, *args, **kwargs):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('landing-page')


class DashboardView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html')


class ProfileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        ctx = get_user_data(request)
        return render(request, 'profile.html', ctx)


class EditProfileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        initial_data = get_initial_user_data(request)
        form = EditProfileForm(initial=initial_data)
        ctx = {'form': form}
        return render(request, 'edit_profile.html', ctx)

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            data = {
                'current_user': request.user,
                'username': form.cleaned_data.get('username'),
                'email': form.cleaned_data.get('email'),
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'password': form.cleaned_data.get('password'),
                'new_password': form.cleaned_data.get('new_password'),
                'repeat_new_password': form.cleaned_data.get('repeat_new_password'),
            }

            if verify_edited_user_data(request, data) is True:
                data['current_user'].save()
                EditionDate.objects.create(user=data['current_user'])
                authenticate_and_login_edited_user(request, data)
                ctx = get_user_data(request)
                return render(request, "profile.html", ctx)
            else:
                initial_data = get_initial_user_data(request)
                form = EditProfileForm(initial=initial_data)
                ctx = {'form': form}
                return render(request, 'edit_profile.html', ctx)


class AddNutritionFactsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = AddNutritionFactsForSuperuserForm()
        else:
            form = AddNutritionFactsForUserForm()
        context = {
            'form': form
        }
        return render(request, "add_product.html", context)

    def post(self, request, *args, **kwargs):
        def get_nutrition(product_name):
            completion = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": generate_prompt_nutrition(product_name)}],
                temperature=0.3,
                max_tokens=100,
            )
            return completion.choices[0].message.content

        if request.user.is_superuser:
            form = AddNutritionFactsForSuperuserForm(request.POST)
        else:
            form = AddNutritionFactsForUserForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            product_name = cd['product_name'][0].upper() + cd['product_name'][1:]
            product = json.loads(get_nutrition(product_name))
            product['example'] = cd['example']
            NutritionFacts.objects.create(**product)
            last_product_id = NutritionFacts.objects.all().order_by('pk').last().pk
            return redirect(f'/products/{last_product_id}/')

        return render(request, "add_product.html", ctx)


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        product_list = NutritionFacts.objects.all().order_by('product_name')
        ctx = {"product_list": product_list}
        return render(request, "product_list.html", ctx)


class ProductDetailsView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        product = get_object_or_404(NutritionFacts, pk=id)
        ctx = {
            'product': product,
        }

        return render(request, "product_details.html", ctx)


class AddTrainingView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get_training(self, intensity, trained_part, level_of_experience):
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "user", "content": generate_prompt_training(intensity, trained_part, level_of_experience)}
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        return completion.choices[0].message.content

    def get(self, request, *args, **kwargs):
        form = AddTrainingForm()
        ctx = {
            'form': form
        }
        return render(request, "add_training.html", ctx)

    def post(self, request, *args, **kwargs):
        form = AddTrainingForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            intensity = cd['intensity']
            trained_part = cd['trained_part']
            level_of_experience = cd['level_of_experience']
            training = json.loads(self.get_training(intensity, trained_part, level_of_experience))
            training['intensity'] = intensity
            training['trained_part'] = trained_part
            training['level_of_experience'] = level_of_experience
            Training.objects.create(**training)
            last_training_id = Training.objects.all().order_by('pk').last().pk
            return redirect(f'/trainings/{last_training_id}/')

        return render(request, "add_training.html", ctx)


class TrainingDetailsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        training = get_object_or_404(Training, pk=id)
        ctx = {
            'training': training,
        }

        return render(request, "training_details.html", ctx)


class TrainingListView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        training_list = Training.objects.all().order_by('training_name')
        ctx = {"training_list": training_list}
        return render(request, "training_list.html", ctx)
