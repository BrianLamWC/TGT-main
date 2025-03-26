from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.template import loader
import time
from .forms import NewUserForm, HeightWeightForm, NewWorkoutForm, WorkoutNewValueForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from api.models import Workout, WorkoutEntry, UserWeightHeightEntry
from api.views import UserWeightHeightEntryViewSet, WorkoutEntryViewSet
from api.serializers import UserWeightHeightEntrySerializer, WorkoutSerializer, WorkoutEntrySerializer
import datetime
import random
import math


def is_logged_in(request):
    """
    The is_logged_in function checks to see if the user is logged in. 
    If they are, it returns True. If not, it returns False.

    :param request: Check if the user is logged in
    :return: True if a user is logged in, and false otherwise

    """
    return not request.user.is_anonymous and request.user.is_authenticated


def login_view(request):
    """
    The login_view function is used to log in a user. If the user is already logged in, they are redirected to the home page. If not, they are asked for their username and password and then authenticated. Once authenticated, they are logged in.

    :param request: Get the user's input from the login form
    :return: The authenticationform class

    """
    if is_logged_in(request):
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login/login.html", context={"login_form": form})


def logout_view(request):
    """
    The logout_view function logs the user out and redirects them to the index page.


    :param request: Pass the request object to the function
    :return: A httpresponseredirect object, which is a type of response that redirects the user to a different page

    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


def register_view(request):
    """
    The register_view function creates a new user and logs them in.
    It also displays success or error messages to the user.

    :param request: Check if the request is a post or get
    :return: A newuserform object

    """
    if not request.user.is_anonymous and request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="login/register.html", context={"register_form": form})


def getWorkout(name):
    """
    The getWorkout function returns a workout object from the database.
       If no workout is found, it returns None.

    :param name: Filter the workouts by name
    :return: A workout object

    """
    workouts = list(Workout.objects.filter(name=name))
    if len(workouts) > 0:
        return workouts[0]

    return None


def create_new_workout_entry(request, data):
    """
    The create_new_workout_entry function creates a new workout entry for the user.
    It takes in a request and data as parameters. It then gets the workout by name, checks if it exists, and creates it if not. 
    If the workout exists, we get that instance of Workout model from our database using getWorkout the function defined above. 
    We then create an object with all of our required data to be pushed to our database using the serializer.

    :param request: The request
    :param data: data containing workout_name, workout_value and user_id

    """
    # Get the workout by the name
    workout_name = data['workout_name']
    workoutInstance = getWorkout(workout_name)
    if workoutInstance is None:
        # We create the workout
        wData = {'name': workout_name}
        wS = WorkoutSerializer(data=wData)
        if wS.is_valid():
            wS.save()
            workoutInstance = getWorkout(workout_name)

        else:
            messages.error(request, wS.errors)
            return

    if workoutInstance is not None:
        # Creating the data object for the serializer
        nData = {
            "workout_id": workoutInstance.id,
            "user_id": data["user_id"],
            "workout_value": data["workout_value"],
            "workout_time": datetime.datetime.now()
        }

        serializer = WorkoutEntrySerializer(None, nData)
        if serializer.is_valid():
            # Pushing to the database
            serializer.save()
            messages.info(request, "Successfully added new workout entry.")
        else:
            messages.error(request, serializer.errors)
    else:
        messages.error(request, "Internal error while creating the workout!")


def get_all_workout_names():
    """
    The get_all_workout_names function grabs all the workouts from the database and creates a dictionary with their id as key and name as value.

    :return: A dictionary with the workout id as the key and the workout name as the value

    """
    # Grabbing all workouts
    workouts = Workout.objects.all()
    # Creating workout names dictionary
    workout_names = {}
    for workout in workouts:
        workout_names[workout.id] = workout.name

    return workout_names


def home_view(request):
    """
    The home_view function is responsible for rendering the home/progress page.
    It does this by loading the template 'home/home.html' and passing it a context object containing:
        - workout_datas: A list of dictionaries, each representing a workout with keys &quot;name&quot;, &quot;name_sanitized&quot;, &quot;data1&quot; (the value points), and &quot;data2&quot (the date points);. The values are in the HTML templates to render graphs.
        - add_data_point_form: An instance of WorkoutNewValueForm which is used to create new entries on POST requests.

    :param request: The request

    """
    if not is_logged_in(request):
        return redirect('login')

    if request.method == "POST":
        # A new workout entry was added
        data = {
            "user_id": request.user.id,
            "workout_name": request.POST.get('workout_name'),
            "workout_value": request.POST.get('workout_value'),
        }
        create_new_workout_entry(request, data)
        return redirect("home")

    template = loader.get_template('home/home.html')

    # Grabbing the users workout entries
    workout_entries = WorkoutEntry.objects.filter(user=request.user)
    workout_names = get_all_workout_names()

    # Creating presentable data for the template
    workout_data_raw = {}
    for entry in workout_entries:
        wId = entry.workout_id
        if wId not in workout_data_raw:
            workout_data_raw[wId] = {
                "data1": [],
                "data2": [],
            }

        wdr = workout_data_raw[wId]
        wdr["data1"].append(entry.workout_time.strftime("%Y-%m-%d %H:%M:%S"))
        wdr["data2"].append(entry.workout_value)

    workout_names = get_all_workout_names()
    workout_datas = []
    for workout_id in workout_data_raw:
        workout_name = workout_names[workout_id]
        workout_data = workout_data_raw[workout_id]
        workout_datas.append(
            {
                "name": workout_name,
                "name_sanitized": workout_name.replace(" ", "_"),
                "data1": workout_data["data1"],
                "data2": workout_data["data2"]
            }
        )

    add_data_point_form = WorkoutNewValueForm()
    context = {
        "workout_datas": workout_datas,
        "add_data_point_form": add_data_point_form
    }

    return HttpResponse(template.render(context, request))


def profile_view(request):
    """
    The profile_view function is used to render the profile page. It takes a request object as an argument and returns a template containing the last recorded weight/height entry for that user, along with their BMI.
    :param request: The request

    """
    if not is_logged_in(request):
        return redirect('login')

    template = loader.get_template('profile/profile.html')

    allEntries = UserWeightHeightEntry.objects.filter(user=request.user)
    lastEntry = allEntries.last()

    bmi_entries = {
        "x": [],
        "y": []
    }

    for entry in allEntries:
        bmi_entries["x"].append(
            entry.recorded_time.strftime("%Y-%m-%d %H:%M:%S"))
        bmi_entries["y"].append(entry.user_bmi)

    context = {"lastEntry": lastEntry, "bmi_entries": bmi_entries}
    return HttpResponse(template.render(context, request))


def bmi_form_view(request):
    """
    The bmi_form_view function is used to create a form for the user to enter their weight and height.
    It then calculates the BMI of the user and stores it in a database.

    :param request: The request

    """
    if not is_logged_in(request):
        return redirect('login')

    if request.method == "POST":
        bmiForm = HeightWeightForm(request.POST)
        if bmiForm.is_valid():
            weight = bmiForm.cleaned_data.get('weight')
            height = bmiForm.cleaned_data.get('height')
            data = {
                "user_id": request.user.id,
                "user_weight": weight,
                "user_height": height,
                "user_bmi": round(weight/(height/100)**2, 2),
                "recorded_time": datetime.datetime.now()
            }

            # # Test data
            # end = datetime.datetime.now()
            # start = end - datetime.timedelta(days=180)
            # toImprove = 20
            # stepValue = toImprove / 180
            # startValue = weight + toImprove
            # print(toImprove, stepValue, startValue)
            # for i in range(180):
            #     randomTime = start + datetime.timedelta(days=i)
            #     value = (startValue - (i * stepValue)) * \
            #         (0.97 + random.random() * 0.06)
            #     nData = {
            #         "user_id": request.user.id,
            #         "user_weight": value,
            #         "user_height": height,
            #         "user_bmi": round(value/(height/100)**2, 2),
            #         "recorded_time": randomTime
            #     }

            #     print(nData)
            #     serializer = UserWeightHeightEntrySerializer(None, nData)
            #     if serializer.is_valid():
            #         # Pushing to the database
            #         serializer.save()

            serializer = UserWeightHeightEntrySerializer(
                None, data)  # deserialize
            if not serializer.is_valid():
                messages.error(request, "Error serializing WeightHeightEntry")
            else:
                serializer.save()
                messages.info(request, "BMI info successfully entered")
                return redirect('profile')

    bmiForm = HeightWeightForm()
    return render(request=request, template_name="bmi_form/bmi_form.html", context={"bmi_form": bmiForm})


def new_workout_view(request):
    """
    The new_workout_view function is used to create a new workout entry in the database.
    It takes a request object as an argument and returns the home page if successful, otherwise it returns the new_workout page.

    :param request: The request
    """
    if not is_logged_in(request):
        return redirect('login')

    if request.method == "POST":
        form = NewWorkoutForm(request.POST)
        if form.is_valid():
            workout_name = form.cleaned_data.get('workout_name')
            workout_value = form.cleaned_data.get('workout_value')
            data = {
                "user_id": request.user.id,
                "workout_name": workout_name,
                "workout_value": workout_value
            }
            create_new_workout_entry(request, data)
            return redirect("home")

    form = NewWorkoutForm()
    return render(request=request, template_name="new_workout_form/new_workout_form.html", context={"new_workout_form": form})


def test_view(request):
    template = loader.get_template('test/test.html')
    context = {}
    return HttpResponse(template.render(context, request))
