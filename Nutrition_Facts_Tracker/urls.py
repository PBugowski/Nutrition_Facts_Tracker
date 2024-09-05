"""
URL configuration for Nutrition_Facts_Tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.urls import path
from Nutrition_Facts_Tracker_App import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.LandingPageView.as_view(), name='landing-page'),
    path('register/', app_views.RegisterUserView.as_view(), name='register'),
    path('login/', app_views.LoginUserView.as_view(), name='login'),
    path('logout/', app_views.LogoutUserView.as_view(), name='logout'),
    path('dashboard/', app_views.DashboardView.as_view(), name='dashboard'),
    path('products/', app_views.ProductListView.as_view(), name='products'),
    path('trainings/', app_views.TrainingListView.as_view(), name='trainings'),
    path('profile/', app_views.ProfileView.as_view(), name='profile'),
    path('add_product/', app_views.AddNutritionFactsView.as_view(), name='add-product'),
    # path('add_meal/', app_views.LogoutUserView.as_view(), name='add-meal'),
    # path('add_plan/', app_views.LogoutUserView.as_view(), name='add-plan'),
    path('add_training/', app_views.AddTrainingView.as_view(), name='add-training'),
    # path('todays_goal/', app_views.LogoutUserView.as_view(), name='todays-goal'),
    path('edit_profile/', app_views.EditProfileView.as_view(), name='edit-profile'),
    path('products/<int:id>/', app_views.ProductDetailsView.as_view(), name='product-details'),
    path('trainings/<int:id>/', app_views.TrainingDetailsView.as_view(), name='training-details'),
]
