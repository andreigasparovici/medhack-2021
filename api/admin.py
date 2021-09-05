from django.contrib import admin

from .models import (
    Diagnostic,
    Comorbidity,
    Person,
    MealType,
    Food,
)


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    pass


@admin.register(Comorbidity)
class ComorbidityAdmin(admin.ModelAdmin):
    pass


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
