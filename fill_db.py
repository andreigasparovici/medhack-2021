import sys

import openfoodfacts

from pprint import pprint as pp
from api.models import Food

def search_and_add(q):
    objs = [obj for obj in openfoodfacts.products.search(q)['products'] if obj.get('generic_name','')]
    if not objs:
        return

    obj = objs[0]

    name = obj['generic_name']

    Food.objects.create(
        name=obj['generic_name'],
        proteins_100g=obj['nutriments']['proteins_100g'],
        carbohydrates_100g=obj['nutriments']['carbohydrates_100g'],
        sugars_100g=obj['nutriments']['sugars_100g'],
        fat_100g=obj['nutriments']['fat_100g'],
        saturated_fat_100g=obj['nutriments']['saturated-fat_100g'],
        fiber_100g=obj['nutriments'].get('fiber_100g', 0),
        is_vegetarian=False
    )


for q in []:
    search_and_add(q)
