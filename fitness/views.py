from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Workout, Exercise
from .serializers import WorkoutSerializer, ExerciseSerializer

# Create your views here.


def home(request):
    workouts = Workout.objects.all()
    return render(request, "home.html", {"workouts": workouts})


def add_workout(request):
    if request.method == "POST":
        Workout.objects.create(name=request.POST["name"])
        return redirect("home")
    return render(request, "add_workout.html")


def add_exercise(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    if request.method == "POST":
        Exercise.objects.create(
            workout=workout,
            name=request.POST["name"],
            calories_burned=request.POST["calories"]
        )
        return redirect("home")
    return render(request, "add_exercise.html", {"workout": workout})


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer