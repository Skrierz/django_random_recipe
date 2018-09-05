from django.shortcuts import render, get_object_or_404
from recipes.models import Dish
import random


def index(request):
    if request.method == 'POST':
        id_list = []
        all_dishes = Dish.objects.values('pk')
        for dish_id in all_dishes:
            id_list.append(dish_id['pk'])
        random_dish_id = random.choice(id_list)
        dish = get_object_or_404(Dish, pk=random_dish_id)
        return render(request, 'mainpage/index.html', {
            'dish': dish
            })
    else:
        return render(request, 'mainpage/index.html')
