# Generated by Django 5.1.1 on 2024-11-28 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warhammer', '0005_remove_operativegun_gun_operativegun_gun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customarmy',
            name='army',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warhammer.army'),
        ),
        migrations.AlterField(
            model_name='customarmy',
            name='operative',
            field=models.ManyToManyField(blank=True, null=True, to='warhammer.operativegun'),
        ),
        migrations.AlterField(
            model_name='operativegun',
            name='gun',
            field=models.ManyToManyField(blank=True, null=True, to='warhammer.gun'),
        ),
        migrations.AlterField(
            model_name='operativegun',
            name='operative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warhammer.operative'),
        ),
    ]
