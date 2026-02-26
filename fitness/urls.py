from django.urls import path, include
from .views import (
     home,
    add_workout,
    add_exercise,
    delete_exercise,
    delete_workout,
    edit_workout,
    signup_view,
    login_view,
    logout_view,
    exercise_templates,
    add_exercise_template,
    calendar_view,
)


urlpatterns = [
    # pages
    path("", home, name="home"),
    path("add-workout/", add_workout, name="add_workout"),
    path("add-exercise/<int:workout_id>/", add_exercise, name="add_exercise"),
    path("delete-exercise/<int:exercise_id>/", delete_exercise, name="delete_exercise"),
    path("edit-workout/<int:workout_id>/", edit_workout, name="edit_workout"),
    path("calendar/", calendar_view, name="calendar"),
    path("delete-workout/<int:workout_id>/", delete_workout, name="delete_workout"),
    path("templates/", exercise_templates, name="exercise_templates"),
    path("templates/add/", add_exercise_template, name="add_exercise_template"),
    

    # auth
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

]