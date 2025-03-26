from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import WorkoutEntry, Workout, UserWeightHeightEntry


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name']


class WorkoutEntrySerializer(serializers.ModelSerializer):
    workout_value = serializers.FloatField()
    workout_time = serializers.DateTimeField()
    workout_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = WorkoutEntry
        fields = ['workout_id', 'user_id', 'workout_value', 'workout_time']

    # def create(self, validated_data):
    #     obj = WorkoutEntry.objects.create(**validated_data)
    #     return obj

class UserWeightHeightEntrySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    user_weight = serializers.FloatField()
    user_height = serializers.FloatField()
    user_bmi = serializers.FloatField()
    recorded_time = serializers.DateTimeField()

    class Meta:
        model = UserWeightHeightEntry
        fields = ['user_id', 'user_weight', 'user_height', 'recorded_time', 'user_bmi']
