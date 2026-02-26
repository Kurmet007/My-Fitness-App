from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import (
    Workout,
    Exercise,
    ExerciseTemplate,
)
from .serializers import WorkoutSerializer, ExerciseSerializer


# -----------------------
# AUTH VIEWS
# -----------------------

def signup_view(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        return redirect("login")
    return render(request, "signup.html")


def login_view(request):
    error = None

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )

        if user:
            login(request, user)
            return redirect("home")
        else:
            error = "Account does not exist or password is incorrect."

    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


# -----------------------
# APP VIEWS (PROTECTED)
# -----------------------

@login_required(login_url="/login/")
def home(request):
    day = request.GET.get("day")

    workouts = Workout.objects.filter(user=request.user)

    if day:
        workouts = workouts.filter(day=day)

    return render(
        request,
        "home.html",
        {
            "workouts": workouts,
            "selected_day": day,
        },
    )


@login_required(login_url="/login/")
def add_workout(request):
    if request.method == "POST":
        Workout.objects.create(
            user=request.user,
            name=request.POST["name"],
            day=request.POST["day"],
        )
        return redirect("home")

    return render(request, "add_workout.html")


@login_required(login_url="/login/")
def add_exercise(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    templates = ExerciseTemplate.objects.filter(user=request.user)

    if request.method == "POST":
        template = ExerciseTemplate.objects.get(
            id=request.POST["template_id"],
            user=request.user,
        )

        Exercise.objects.create(
            workout=workout,
            name=template.name,
            sets=template.sets,
            reps=template.reps,
            calories_burned=template.calories_burned,
        )

        return redirect("home")

    return render(
        request,
        "add_exercise.html",
        {"workout": workout, "templates": templates},
    )


@login_required(login_url="/login/")
def delete_exercise(request, exercise_id):
    exercise = Exercise.objects.get(
        id=exercise_id,
        workout__user=request.user,
    )

    if request.method == "POST":
        exercise.delete()
        return redirect("home")


@login_required(login_url="/login/")
def delete_workout(request, workout_id):
    workout = Workout.objects.get(
        id=workout_id,
        user=request.user,
    )

    if request.method == "POST":
        workout.delete()
        return redirect("home")


@login_required(login_url="/login/")
def edit_workout(request, workout_id):
    workout = Workout.objects.get(
        id=workout_id,
        user=request.user,
    )

    if request.method == "POST":
        workout.name = request.POST["name"]
        workout.day = request.POST["day"]
        workout.save()
        return redirect("home")

    return render(request, "edit_workout.html", {"workout": workout})


@login_required
def add_exercise_template(request):
    if request.method == "POST":
        ExerciseTemplate.objects.create(
            user=request.user,
            name=request.POST["name"],
            sets=request.POST["sets"],
            reps=request.POST["reps"],
            calories_burned=request.POST["calories"],
        )
        return redirect("exercise_templates")

    return render(request, "add_exercise_template.html")


@login_required
def exercise_templates(request):
    templates = ExerciseTemplate.objects.filter(user=request.user)
    return render(
        request,
        "exercise_templates.html",
        {"templates": templates},
    )


# -----------------------
# API VIEWS
# -----------------------

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


# -----------------------
# CALENDAR VIEW
# -----------------------

@login_required(login_url="/login/")
def calendar_view(request):
    workouts = Workout.objects.filter(user=request.user)

    days = {
        "Monday": workouts.filter(day="mon"),
        "Tuesday": workouts.filter(day="tue"),
        "Wednesday": workouts.filter(day="wed"),
        "Thursday": workouts.filter(day="thu"),
        "Friday": workouts.filter(day="fri"),
        "Saturday": workouts.filter(day="sat"),
        "Sunday": workouts.filter(day="sun"),
    }

    return render(request, "calendar.html", {"days": days})