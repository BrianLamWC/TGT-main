from cProfile import label
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class HeightWeightForm(forms.Form):
    height = forms.FloatField(label='Height(cm)', max_value=200)
    weight = forms.FloatField(label='Weight(kg)', max_value=300)


class NewWorkoutForm(forms.Form):
    workout_name = forms.CharField(label='Workout Name', max_length=255)
    workout_value = forms.FloatField(label='Start Value')


class WorkoutNewValueForm(forms.Form):
    workout_value = forms.FloatField(label='Current Value')
