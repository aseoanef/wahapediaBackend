# Generated by Django 5.1.1 on 2024-12-01 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warhammer', '0004_remove_army_ability_army_ability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='army',
            name='ability',
            field=models.ManyToManyField(to='warhammer.ability'),
        ),
        migrations.AlterField(
            model_name='army',
            name='name',
            field=models.CharField(max_length=240, unique=True),
        ),
    ]