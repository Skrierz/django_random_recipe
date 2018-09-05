from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Dish


def index(request, page=1):
    dishes_on_page = 20
    paginator = Paginator(Dish.objects.all(), dishes_on_page)
    last_page = paginator.num_pages
    dishes = paginator.get_page(page)
    template_dict = {
        'page': page,
        'dishes': dishes,
        'last_page': last_page
    }
    return render(request, 'recipes/index.html', template_dict)
