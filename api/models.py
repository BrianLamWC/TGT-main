from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class WorkoutEntry(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_value = models.FloatField()
    workout_time = models.DateTimeField()


class UserWeightHeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_weight = models.FloatField()
    user_height = models.FloatField()
    user_bmi = models.FloatField()
    recorded_time = models.DateTimeField()
