from django.db import models
from django.forms import ModelForm


class Dish(models.Model):
    name = models.CharField(max_length=128, unique=True)
    recipe_url = models.URLField()
    portions = models.IntegerField()

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

    name = models.CharField(max_length=24, unique=True, choices=type_choices)

    def __str__(self):
        return self.get_name_display()


class Ingredient(models.Model):
    name = models.CharField(max_length=48, unique=True)
    amount_type = models.ForeignKey('Type', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IngredientDish(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    default_amount = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.dish.name, self.ingredient.name)


class Recount(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('IngredientDish', on_delete=models.CASCADE)
    user_portions = models.IntegerField(blank=True, null=True, default=None)
    total_amount = models.IntegerField(blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if self.user_portions is None or self.user_portions <= 0:
            self.user_portions = self.ingredient.default_amount
        amount_per_portion = self.ingredient.default_amount/self.dish.portions
        self.total_amount = amount_per_portion * self.user_portions
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.ingredient, self.total_amount)









class RecipeForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'recipe_url']
