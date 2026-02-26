from django.db import models

# Create your models here.


class Workout(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        related_name="exercises",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    calories_burned = models.PositiveIntegerField()

    def __str__(self):
        return self.name