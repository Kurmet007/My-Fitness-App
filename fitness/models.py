id="daymdl"
from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):

    DAYS_OF_WEEK = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    day = models.CharField(
        max_length=3,
        choices=DAYS_OF_WEEK
    )

    def total_calories(self):
        return sum(
            ex.calories_burned for ex in self.exercises.all()
        )

    def __str__(self):
        return f"{self.name} ({self.get_day_display()})"


class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        related_name="exercises",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    calories_burned = models.IntegerField()

    def __str__(self):
        return self.name


class ExerciseTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    calories_burned = models.IntegerField()

    def __str__(self):
        return self.name