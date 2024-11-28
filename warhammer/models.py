from django.db import models

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
    unique_action = models.ManyToManyField('UniqueAction',blank=True)
    gun = models.ManyToManyField('Gun',blank=True)
    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "stats":{
                "movement": self.movement,
                "dash": self.dash,
                "apl": self.apl,
                "ga": self.ga,
                "df": self.df,
                "sv": self.sv,
                "w": self.w,
                "base": self.base,
            },
        }


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
    special_rule = models.ManyToManyField('SpecialRule',blank=True)
    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "stats": {
                "attacks": self.attacks,
                "ws": self.ws,
                "dmg": self.dmg,
                "critical_dmg": self.critical_dmg,
            },
        }


class SpecialRule(models.Model):
    name = models.CharField(max_length=240)
    description = models.CharField(max_length=1000)
    modifier = models.IntegerField(blank=True,null=True)
    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "description": self.description,
            "modifier": self.modifier,
        }


class Army(models.Model):
    name = models.CharField(max_length=240,null=False,)
    operatives = models.ManyToManyField('Operative')
    ability = models.ForeignKey('Ability', blank=True, on_delete=models.DO_NOTHING)
    faction = models.CharField(max_length=240,)


class CustomArmy(models.Model):
    name = models.CharField(max_length=240,null=False)
    army = models.ForeignKey('Army',on_delete=models.CASCADE)
    operative = models.ManyToManyField('OperativeGun')


class OperativeGun(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)
    operative = models.ForeignKey('Operative',on_delete=models.CASCADE,blank=True,null=True)
    gun = models.ManyToManyField('Gun')


class Ability(models.Model):
    name = models.CharField(max_length=240,)
    description = models.CharField(max_length=1000)
    cost = models.IntegerField()