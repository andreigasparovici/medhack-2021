import datetime
import enum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


class Diagnostic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comorbidity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "comorbidities"


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birthday = models.DateField()

    sex = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()

    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    comorbidities = models.ManyToManyField(Comorbidity)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def _bmi_value(self):
        return self.weight / self.height ** 2

    class BMI(enum.Enum):
        UNDERWEIGHT = 0
        NORMAL = 1
        OVERWEIGHT = 2
        OBESE = 3
        EXTREMELY_OBESE = 4

    def bmi(self) -> BMI:
        value = self._bmi_value()
        if value < 18.5:
            return Person.BMI.UNDERWEIGHT
        elif value < 24.9:
            return Person.BMI.NORMAL
        elif value < 29.9:
            return Person.BMI.OVERWEIGHT
        elif value < 34.9:
            return Person.BMI.OBESE
        else:
            return Person.BMI.EXTREMELY_OBESE

    def daily_energy(self):
        bmi = self.bmi()
        if bmi == Person.BMI.NORMAL:
            return 0.9 * self.weight * 24
        elif bmi == Person.BMI.UNDERWEIGHT:
            return 1.3 * self.weight * 24
        else:
            return 0.75 * self.weight * 24


class MealType(models.Model):
    name = models.CharField(max_length=50)
    energy_percentage = models.FloatField(validators=[
        MinValueValidator(0),
        MaxValueValidator(1),
    ])
    is_main_meal = models.BooleanField(default=False, verbose_name="Main meal")

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    types = models.ManyToManyField(MealType)

    proteins_100g = models.FloatField()
    carbohydrates_100g = models.FloatField()
    sugars_100g = models.FloatField()
    fat_100g = models.FloatField()
    saturated_fat_100g = models.FloatField()
    fiber_100g = models.FloatField()

    is_vegetarian = models.BooleanField(default=False, verbose_name="Vegetarian")

    def __str__(self):
        return self.name



