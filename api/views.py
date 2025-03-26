from api.models import WorkoutEntry, Workout, UserWeightHeightEntry
from api.serializers import WorkoutEntrySerializer, WorkoutSerializer, UserSerializer, UserWeightHeightEntrySerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from django.contrib.auth.models import User, Group
import datetime
import random
from random import randrange
from datetime import timedelta


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]


def getWorkout(name):
    """
    The getWorkout function returns a workout object from the database. If no matching workout is found, it returns None.

    :param name: Filter the workout objects
    :return: The workout with the name passed in as an argument
    """
    workouts = list(Workout.objects.filter(name=name))
    if len(workouts) > 0:
        return workouts[0]

    return None


class WorkoutEntryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutEntry.objects.filter(user=self.request.user)


class UserWeightHeightEntryViewSet(viewsets.ModelViewSet):
    serializer_class = UserWeightHeightEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserWeightHeightEntry.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        The create function is used to create a new instance of the UserWeightHeightEntry model. It takes in a request and returns a response. The data is taken from the request, cleaned up, validated and then saved to the database.

        :param self: Reference the class instance itself
        :param request: The request to the REST API
        :param *args: Send a non-keyworded variable length argument list to the function (Not used)
        :param **kwargs: Pass in any extra keyword arguments that are passed to the function (Not used)
        :return: Response containing either the error messages of the serializer or the data of the new model instance
        """
        data = request.data.copy()
        user_id = request.user.id
        data = {
            "user_id": user_id,
            "user_weight": data.pop('user_weight'),
            "user_height": data.pop('user_height'),
            "user_bmi": data.pop('user_bmi'),
            "recorded_time": data.pop('recorded_time')
        }

        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
