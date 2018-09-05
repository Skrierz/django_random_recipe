from django.shortcuts import render, get_object_or_404
from recipes.models import Dish


def index(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    dish_dict = {
        'dish': dish
    }
    return render(request, 'recipe/index.html', dish_dict)
