# Generated by Django 2.1 on 2018-08-23 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testovaya', '0002_auto_20180823_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='recount',
            name='ingredient',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='testovaya.Ingredient'),
            preserve_default=False,
        ),
    ]
