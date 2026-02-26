from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, add_workout, add_exercise, WorkoutViewSet, ExerciseViewSet

router = DefaultRouter()
router.register('workouts', WorkoutViewSet)
router.register('exercises', ExerciseViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('add-workout/', add_workout, name='add_workout'),
    path('add-exercise/<int:workout_id>/', add_exercise, name='add_exercise'),
    path('api/', include(router.urls)),
]