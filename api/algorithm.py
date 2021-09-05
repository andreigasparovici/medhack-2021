import random
from typing import List

import numpy as np
import cvxpy as cp

from .models import Food, MealType

PROTEIN_KCAL = 4
CARB_KCAL = 4
FAT_KCAL = 9


class MealProblem:
    def __init__(self, foods: List[Food], meal_type: MealType, energy_per_day: float, coefficient=1):
        # self.foods = foods.order_by('?')[:5]
        # print(self.foods)
        self.foods = foods

        self.coefficient = coefficient

        self.meal_type = meal_type

        self._var = cp.Variable((len(self.foods),), nonneg=True)
        self.required_energy = energy_per_day * meal_type.energy_percentage

        self._proteins = np.array([f.proteins_100g for f in self.foods]) / 100
        self._proteins_from_vegetarian = np.array([f.proteins_100g if f.is_vegetarian else 0 for f in self.foods]) / 100
        self._carbs = np.array([f.carbohydrates_100g for f in self.foods]) / 100
        self._sugars = np.array([f.sugars_100g for f in self.foods]) / 100
        self._fats = np.array([f.fat_100g for f in self.foods]) / 100
        self._saturated_fats = np.array([f.saturated_fat_100g for f in self.foods]) / 100
        self._fiber = np.array([f.fiber_100g for f in self.foods]) / 100

    @property
    def proteins(self):
        return self._proteins @ self._var

    @property
    def proteins_value(self):
        return self._proteins @ self.value

    @property
    def proteins_from_vegetarian(self):
        return self._proteins_from_vegetarian @ self._var

    @property
    def carbs(self):
        return self._carbs @ self._var

    @property
    def carbs_value(self):
        return self._carbs @ self.value

    @property
    def sugars(self):
        return self._sugars @ self._var

    @property
    def fiber(self):
        return self._fiber @ self._var

    @property
    def fats(self):
        return self._fats @ self._var

    @property
    def fats_value(self):
        return self._fats @ self.value

    @property
    def saturated_fats(self):
        return self._saturated_fats @ self._var

    @property
    def energy(self):
        return PROTEIN_KCAL * self.proteins + CARB_KCAL * self.carbs + FAT_KCAL * self.fats

    @property
    def energy_value(self):
        return PROTEIN_KCAL * self.proteins_value + CARB_KCAL * self.carbs_value + FAT_KCAL * self.fats_value

    def energy_food_value(self, index):
        quantity = self.value[index]
        return quantity * (PROTEIN_KCAL * self._proteins[index]
                           + CARB_KCAL * self._carbs[index] + FAT_KCAL * self._fats[index])

    @property
    def value(self):
        return self._var.value

    @property
    def constraints(self):
        return [
            # Use at least 90% of recommended energy
            self.energy >= .9 * self.required_energy,
            self.energy <= 1.1 * self.required_energy,

            self._var <= 200
        ]

    @property
    def objective(self,
                  penalize_energy_difference=200,
                  penalize_sparsity=50,
                  penalize_large=50,
                  penalize_protein_carb_difference=5000):
        terms = [
            # Minimize difference between actual energy and required energy
            penalize_energy_difference * cp.atoms.norm1(self.energy - self.required_energy),

            # Promote sparsity
            penalize_sparsity * cp.atoms.norm1(self._var),

            # Promote small values
            penalize_large * cp.atoms.norm_inf(self._var),

            # Minimize difference between carbs and proteins
            penalize_protein_carb_difference * cp.atoms.norm1(self.proteins - self.carbs)
        ]
        return sum(terms)


class DayProblem:
    def __init__(self, meal_problems: List[MealProblem], energy_per_day: float):
        self.meal_problems = meal_problems
        self.required_energy = energy_per_day

    @property
    def _constraints(self):
        return sum([problem.constraints for problem in self.meal_problems], []) + [
            # At least 25g fiber daily
            self.fiber >= 25,

            # Energy from protein should be between 15% and 20% of total
            PROTEIN_KCAL * self.proteins >= .15 * self.required_energy,
            PROTEIN_KCAL * self.proteins <= .20 * self.required_energy,

            # Energy from carbs should be between 45% and 55% of total
            CARB_KCAL * self.carbs >= .45 * self.required_energy,
            CARB_KCAL * self.carbs <= .55 * self.required_energy,

            # Energy from fats should be between 25% and 35% of total
            FAT_KCAL * self.fats >= .25 * self.required_energy,
            FAT_KCAL * self.fats <= .35 * self.required_energy,

            # Protein should be >= 1/2 from vegetable sources
            self.proteins_from_vegetarian >= self.proteins / 2,

            # Saturated fats should be less than 1/4 of total fats
            self.saturated_fats <= self.fats / 4,
        ]

    @property
    def proteins(self):
        return sum([p.proteins for p in self.meal_problems])

    @property
    def proteins_from_vegetarian(self):
        return sum([p.proteins_from_vegetarian for p in self.meal_problems])

    @property
    def carbs(self):
        return sum([p.carbs for p in self.meal_problems])

    @property
    def sugars(self):
        return sum([p.sugars for p in self.meal_problems])

    @property
    def fiber(self):
        return sum([p.fiber for p in self.meal_problems])

    @property
    def fats(self):
        return sum([p.fats for p in self.meal_problems])

    @property
    def saturated_fats(self):
        return sum([p.saturated_fats for p in self.meal_problems])

    @property
    def _objective(self):
        return cp.Minimize(
            sum([problem.objective for problem in self.meal_problems])
        )

    @property
    def _problem(self):
        return cp.Problem(self._objective, self._constraints)

    def solve(self):
        problem = self._problem
        problem.solve()
        return problem.status
