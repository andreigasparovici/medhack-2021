from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


from .algorithm import MealProblem, DayProblem

from .models import Diagnostic, Comorbidity, Food, Person, MealType
from .serializers import (
    DiagnosticSerializer,
    ComorbiditySerializer,
    PersonSerializer,
)


class DiagnosticsList(ListAPIView):
    queryset = Diagnostic.objects.all()
    serializer_class = DiagnosticSerializer


class ComorbiditiesList(ListAPIView):
    queryset = Comorbidity.objects.all()
    serializer_class = ComorbiditySerializer


@api_view(http_method_names=["POST"])
def register(request):
    person = PersonSerializer(data=request.data)
    person.is_valid(raise_exception=True)
    person.save()
    return HttpResponse("", status=status.HTTP_201_CREATED)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def test_auth(request):
    return HttpResponse("OK")


PROTEIN_KCAL = 4
CARB_KCAL = 4
FAT_KCAL = 9


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def generate_menu(request):
    person = Person.objects.get(user__pk=request.user.pk)

    breakfast = MealType.objects.get(pk=1)
    snack = MealType.objects.get(pk=2)
    lunch = MealType.objects.get(pk=3)
    dinner = MealType.objects.get(pk=4)

    breakfast_problem = MealProblem(
        foods=Food.objects.filter(types__pk=breakfast.pk),
        meal_type=breakfast,
        energy_per_day=person.daily_energy(),
        # coefficient=200
    )

    first_snack_problem = MealProblem(
        foods=Food.objects.filter(types__pk=snack.pk),
        meal_type=snack,
        energy_per_day=person.daily_energy(),
    )

    lunch_problem = MealProblem(
        foods=Food.objects.filter(types__pk=lunch.pk),
        meal_type=lunch,
        energy_per_day=person.daily_energy(),
        # coefficient=200
    )

    second_snack_problem = MealProblem(
        foods=Food.objects.filter(types__pk=snack.pk),
        meal_type=snack,
        energy_per_day=person.daily_energy(),
    )

    dinner_problem = MealProblem(
        foods=Food.objects.filter(types__pk=dinner.pk),
        meal_type=dinner,
        energy_per_day=person.daily_energy(),
        # coefficient=200
    )

    meal_problems = [
        breakfast_problem,
        first_snack_problem,
        lunch_problem,
        second_snack_problem,
        dinner_problem
    ]

    problem = DayProblem(meal_problems, person.daily_energy())
    problem_status = problem.solve()

    if problem_status in ["infeasible", "unbounded"]:
        return HttpResponse(f"Could not solve")

    response = [
        {
            'name': problem.meal_type.name,
            'meals': [
                {'name': food.name, 'quantity': round(problem.value[i]), 'calories': round(problem.energy_food_value(i))}
                for (i, food) in enumerate(problem.foods)
                if abs(problem.value[i]) > 1e-3
            ]
        }
        for problem in meal_problems
    ]

    return JsonResponse(response, safe=False)
