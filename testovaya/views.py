from django.shortcuts import render
import json
from .models import Dish, IngredientDish, Ingredient, Recipe, Type
import import_to_db


def index(request):
    if request.method == 'POST':
        # print(request.POST['text'])
        with open('recipes.json', encoding='utf-8-sig') as fp:
            data_file = json.load(fp)
        import_to_db.add_new_dish_to_db_from_file(data_file)
    return render(request, 'testovaya/index.html')


'''
    рендер формы
    # if request.method == 'POST':
    #     form = RecipeForm(request.POST)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         form.save()
    # else:
    #     form = RecipeForm()
    # return render(request, 'testovaya/index.html', {'form' : form})
    '''
