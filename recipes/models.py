from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    standart_portions = models.IntegerField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    step = models.CharField(max_length=24)
    action = models.TextField(max_length=500)

    def __str__(self):
        return '{}, шаг № {}'.format(self.dish.name, self.step)


class Type(models.Model):
    L = 'l'
    ML = 'ml'
    KG = 'kg'
    G = 'gram'
    TEASP = 'teasp'
    TABLSP = 'tablsp'
    CUP = 'cup'
    PIECE = 'piece'
    TASTE = 'taste'
    HEAD = 'head'
    JAR = 'jar'
    CHUNK = 'chunk'
    SHEAF = 'sheaf'
    DENTICLE = 'denticle'
    KNIFE = 'knife'
    PINCH = 'pinch'
    STALK = 'stalk'
    type_choices = (
        (L, 'литры'),
        (ML, 'милилитры'),
        (KG, 'килограммы'),
        (STALK, 'стебли'),
        (PINCH, 'щепотки'),
        (KNIFE, 'на кончике ножа'),
        (DENTICLE, 'зубчики'),
        (SHEAF, 'пучки'),
        (CHUNK, 'куски'),
        (JAR, 'банки'),
        (HEAD, 'головки'),
        (TASTE, 'по вкусу'),
        (G, 'граммы'),
        (TEASP, 'чайные ложки'),
        (TABLSP, 'столовые ложки'),
        (CUP, 'стаканы'),
        (PIECE, 'штуки'),
        )

    name = models.CharField(max_length=128, unique=True, choices=type_choices)

    def __str__(self):
        return self.get_name_display()


class Ingredient(models.Model):
    name = models.CharField(max_length=96, unique=True)
    unit_of_mass = models.ForeignKey('Type', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IngredientDish(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.dish.name, self.ingredient.name)
