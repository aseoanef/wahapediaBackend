from django.contrib import admin

# Register your models here.
from .models import Operative,OperativeGun,UniqueAction,Gun,SpecialRule,Army,CustomArmy,Ability

admin.site.register(Operative)
admin.site.register(OperativeGun)
admin.site.register(UniqueAction)
admin.site.register(Gun)
admin.site.register(SpecialRule)
admin.site.register(Army)
admin.site.register(CustomArmy)
admin.site.register(Ability)