from tkinter.constants import CASCADE

from django.db import models
from django.db.models import DO_NOTHING


# Create your models here.
class Operative(models.Model):
    name = models.CharField(max_length=240, )
    movement = models.IntegerField(default=3,)#movement
    dash = models.IntegerField() #dash
    apl = models.IntegerField() #action points limit
    ga = models.IntegerField() #group actions
    df = models.IntegerField() #Defence
    sv = models.IntegerField() #save throw
    w = models.IntegerField() #wounds
    base= models.IntegerField() #base diametro
    unique_action = models.ForeignKey('UniqueAction',blank=True,null=True,on_delete=models.DO_NOTHING)
    gun = models.ForeignKey('Gun',blank=True,on_delete=models.DO_NOTHING)

class UniqueAction(models.Model):
    name = models.CharField(max_length=240,)
    cost = models.IntegerField(default=1,)
    description = models.CharField(max_length=1000,)

class Gun(models.Model):
    name = models.CharField(max_length=240,)
    attacks = models.IntegerField()
    ws = models.IntegerField() #wounds save
    dmg = models.IntegerField() #damage standard
    critical_dmg = models.IntegerField() #critical damage
    special_rule = models.ForeignKey('SpecialRule',blank=True,null=True,on_delete=DO_NOTHING)

class SpecialRule(models.Model):
    name = models.CharField(max_length=240)
    description = models.CharField(max_length=1000)
    modifier = models.IntegerField(blank=True,null=True)

class Army(models.Model):
    name = models.CharField(max_length=240,null=False,)
    operatives = models.ForeignKey('Operative',blank=True,null=True,on_delete=DO_NOTHING)
    ability = models.ForeignKey('Ability', blank=True, on_delete=models.DO_NOTHING)
    faction = models.CharField(max_length=240,)

class CustomArmy(models.Model):
    name = models.CharField(max_length=240,null=False)
    army = models.ForeignKey('Army',on_delete=CASCADE)
    operative = models.ForeignKey('Operative',on_delete=CASCADE)

class OperativeGun(models.Model):
    operative = models.ForeignKey('Operative',on_delete=CASCADE)
    gun = models.ForeignKey('Gun',on_delete=CASCADE)

class Ability(models.Model):
    name = models.CharField(max_length=240,)
    description = models.CharField(max_length=1000)
    cost = models.IntegerField()