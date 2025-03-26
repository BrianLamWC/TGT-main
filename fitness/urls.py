"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from api import views as apiViews

router = routers.DefaultRouter()
router.register(r"workout", apiViews.WorkoutViewSet, basename="workout")
router.register(r"workoutentry", apiViews.WorkoutEntryViewSet,
                basename="workoutentry")
router.register(r"users", apiViews.UserViewSet, basename="users")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('home', views.home_view, name='home'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('home', views.home_view, name='home'),
    path('profile', views.profile_view, name='profile'),
    path('bmi_form', views.bmi_form_view, name='bmi_form'),
    path('new_workout', views.new_workout_view, name='new_workout_'),
    path('logout', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]
