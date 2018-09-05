import json


amounts = []
with open('recipes.json', encoding='utf-8-sig') as fp:
    data_file = json.load(fp)
for recipe_dict in data_file:
    ingredients = recipe_dict['ingredients']
    for key in ingredients.keys():
        if ingredients[key] not in amounts:
            # print(ingredients[key])
            amounts.append(ingredients[key])

types = ['чайн', 'стол', 'стак', 'штук', 'вкус', 'голов', 'банк', 'кус',
         'пуч', 'зубч', 'нож', 'щепот', 'стеб', 'кг', 'мл', 'г', 'л']
new_amounts = []
for i in range(len(amounts)):
    exist = None
    for type_ in types:
        if type_ in amounts[i]:
            exist = True
    if exist is None:
        new_amounts.append(amounts[i])
print(amounts)
print(len(data_file))
