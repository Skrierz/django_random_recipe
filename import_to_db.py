from pprint import pprint
from recipes.models import Dish, Ingredient, Type, IngredientDish, Recipe


def add_new_dish_to_db_from_file(file):
    existed_dish_names = []
    existed_dishes = Dish.objects.values('name')
    for dish in existed_dishes:
        existed_dish_names.append(dish['name'])

    existed_ingredient_names = []
    existed_ingredients = Ingredient.objects.values('name')
    for ingredient in existed_ingredients:
        existed_ingredient_names.append(ingredient['name'])

    for dict_pos in range(len(file)):
        recipe_dict = file[dict_pos]

        new_dish_added = new_dish(recipe_dict, existed_dish_names)
        if new_dish_added:
            existed_dish_names.append(recipe_dict['title'])

        for key in recipe_dict['ingredients'].keys():
            ingredient_amount = recipe_dict['ingredients'][key]

            new_ingredient_added = new_ingredient(key, ingredient_amount,
                                                  existed_ingredient_names)
            if new_ingredient_added:
                existed_ingredient_names.append(key)

            new_ingredient_dish(key, recipe_dict['title'], ingredient_amount)

        new_instruction(recipe_dict['instruction'], recipe_dict['title'])


def new_dish(dict, existed_dish_names):
    if dict['title'] not in existed_dish_names:
        pprint(dict)
        new_dish = Dish()
        new_dish.name = dict['title']
        new_dish.url = dict['url']
        new_dish.standart_portions = int(dict['portions'])
        new_dish.save()
        return True
    else:
        return False


def new_ingredient(ingredient, ingredient_amount, existed_ingredient_names):

        if ingredient not in existed_ingredient_names:
            new_ingredient = Ingredient()
            new_ingredient.name = ingredient
            try:
                ingredient_type = ingredient_amount.split()[1]
            except IndexError as err:
                ingredient_type = ingredient_amount.split()[0]
            type_ = ingredients_type_router(ingredient_type)
            new_ingredient.unit_of_mass = type_
            new_ingredient.save()
            return True
        else:
            return False


def ingredients_type_router(ingredient_type):
    types = ['чайн', 'стол', 'стак', 'штук', 'вкус', 'голов', 'банк', 'кус',
             'пуч', 'зубч', 'конч', 'щепот', 'стеб', 'кг', 'мл', 'г', 'л']
    for type_id in range(len(types)):
        if types[type_id] in ingredient_type:
            if type_id == 0:
                type_ = Type.objects.get(name=Type.TEASP)
            elif type_id == 1:
                type_ = Type.objects.get(name=Type.TABLSP)
            elif type_id == 2:
                type_ = Type.objects.get(name=Type.CUP)
            elif type_id == 3:
                type_ = Type.objects.get(name=Type.PIECE)
            elif type_id == 4:
                type_ = Type.objects.get(name=Type.TASTE)
            elif type_id == 5:
                type_ = Type.objects.get(name=Type.HEAD)
            elif type_id == 6:
                type_ = Type.objects.get(name=Type.JAR)
            elif type_id == 7:
                type_ = Type.objects.get(name=Type.CHUNK)
            elif type_id == 8:
                type_ = Type.objects.get(name=Type.SHEAF)
            elif type_id == 9:
                type_ = Type.objects.get(name=Type.DENTICLE)
            elif type_id == 10:
                type_ = Type.objects.get(name=Type.KNIFE)
            elif type_id == 11:
                type_ = Type.objects.get(name=Type.PINCH)
            elif type_id == 12:
                type_ = Type.objects.get(name=Type.STALK)
            elif type_id == 13:
                type_ = Type.objects.get(name=Type.KG)
            elif type_id == 14:
                type_ = Type.objects.get(name=Type.ML)
            elif type_id == 15:
                type_ = Type.objects.get(name=Type.G)
            elif type_id == 16:
                type_ = Type.objects.get(name=Type.L)
            return type_


def new_ingredient_dish(ingredient_name, dish_name, ingredient_amount):
    dish = Dish.objects.get(name=dish_name)
    ingredient = Ingredient.objects.get(name=ingredient_name)
    new_ingredient_dish = IngredientDish()

    new_ingredient_dish.dish = dish
    new_ingredient_dish.ingredient = ingredient
    ingredient_amount = ingredient_amount.split()[0].replace(',', '.')
    try:
        float(ingredient_amount)
    except ValueError as err:
        print('-----------------------------------------------')
        print(ingredient_amount)
        print('-----------------------------------------------')
        if ingredient_amount == '¼':
            new_ingredient_dish.default_number_of_servings = 0.25
        elif ingredient_amount == 'по':
            new_ingredient_dish.default_number_of_servings = 0
        elif ingredient_amount == '½':
            new_ingredient_dish.default_number_of_servings = 0.5
        elif ingredient_amount == '¾':
            new_ingredient_dish.default_number_of_servings = 0.75
        elif ingredient_amount == 'щепотка' or ingredient_amount == 'на':
            new_ingredient_dish.default_number_of_servings = 1
        elif ingredient_amount == '⅓':
            new_ingredient_dish.default_number_of_servings = 0.33
        elif ingredient_amount == '⅔':
            new_ingredient_dish.default_number_of_servings = 0.66
    else:
        def_num = float(ingredient_amount)
        new_ingredient_dish.default_number_of_servings = def_num
    new_ingredient_dish.save()


def new_instruction(instruction, dish_name):
    dish = Dish.objects.get(name=dish_name)
    for i in range(len(instruction)):
        new_recipe = Recipe()
        new_recipe.dish = dish
        new_recipe.step = i + 1
        new_recipe.action = instruction[i]
        new_recipe.save()
