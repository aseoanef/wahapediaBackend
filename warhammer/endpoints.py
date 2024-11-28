import json
from msvcrt import putch

from django.http import JsonResponse
from .models import Operative, Gun, SpecialRule, UniqueAction, Ability, Army, CustomArmy, OperativeGun
from django.views.decorators.csrf import csrf_exempt


def army(request):
    # Manejar la solicitud GET
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("armyName") != None:
            armyName = request.headers.get("armyName")
            try:
                all_rows = Army.objects.filter(name=armyName)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Army was not found"}, status=404)
            json_response = []
            for row in all_rows:
                operatives = row.operatives.all()
                operativeses = []
                abilitys = row.ability.all()
                abilityses = []
                for operative in operatives:
                    operativeses.append(operative.name)
                for ability in abilitys:
                    abilityses.append(ability.name)
                json_response.append({
                    'id': row.pk,
                    'name': row.name,
                    'faction': row.faction,
                    'operatives': operativeses,
                    'abilities': abilityses,
                })
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = Army.objects.all()
            json_response = []
            for row in all_rows:
                operatives = row.operatives.all()
                operativeses = []
                abilitys = row.ability.all()
                abilityses = []
                for operative in operatives:
                    operativeses.append(operative.name)
                for ability in abilitys:
                    abilityses.append(ability.name)
                json_response.append({
                    'id': row.pk,
                    'name': row.name,
                    'faction': row.faction,
                    'operatives': operativeses,
                    'abilities': abilityses,
                })
        return JsonResponse(json_response, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

#estropeado
def armybyId(request,armyId):
    # Manejar la solicitud GET
    if request.method == 'GET':
        try:
            all_rows = Army.objects.get(pk=armyId)
        except all_rows.DoesNotExist:
            return JsonResponse({"error": "Army was not found"}, status=404)
        json_response = []
        for row in all_rows:
            operatives = row.operatives.all()
            operativeses = []
            abilitys = row.ability.all()
            abilityses = []
            for operative in operatives:
                operativeses.append(operative.name)
            for ability in abilitys:
                abilityses.append(ability.name)
            json_response.append({
                'id': row.pk,
                'name': row.name,
                'faction': row.faction,
                'operatives': operativeses,
                'abilities': abilityses,
            })
        return JsonResponse(json_response, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def operative(request):
    # Manejar la solicitud GET
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("operativeName") != None:
            operativeName = request.headers.get("operativeName")
            try:
                all_rows = Operative.objects.filter(name=operativeName)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Operative was not found"}, status=404)
            json_response = []
            for row in all_rows:
                uniqueactions = row.unique_action.all()
                uniqueactiones = []
                guns = row.gun.all()
                gunes = []
                for gun in guns:
                    gunes.append(gun.name)
                for uniqueaction in uniqueactions:
                    uniqueactiones.append(uniqueaction.name)
                json_response.append({
                    'id': row.pk,
                    'name': row.name,
                    'stats': {
                        'movement': row.movement,
                        'dash': row.dash,
                        'apl': row.apl,
                        'ga': row.ga,
                        'df': row.df,
                        'sv': row.sv,
                        'w': row.w,
                        'base': row.base,
                    },
                    'unique_actions': uniqueactiones,
                    'guns': gunes,
                })
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = Operative.objects.all()
            json_response = []
            for row in all_rows:
                uniqueactions = row.unique_action.all()
                uniqueactiones = []
                guns = row.gun.all()
                gunes = []
                for gun in guns:
                    gunes.append(gun.name)
                for uniqueaction in uniqueactions:
                    uniqueactiones.append(uniqueaction.name)
                json_response.append({
                    'id': row.pk,
                    'name': row.name,
                    'stats': {
                        'movement': row.movement,
                        'dash': row.dash,
                        'apl': row.apl,
                        'ga': row.ga,
                        'df': row.df,
                        'sv': row.sv,
                        'w': row.w,
                        'base': row.base,
                    },
                    'unique_actions': uniqueactiones,
                    'guns': gunes,
                })
        return JsonResponse(json_response, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

#estropeado
def operativebyId(request,operativeId):
    if request.method == "GET":
        try:
            all_rows = Operative.objects.get(pk=operativeId)
        except all_rows.DoesNotExist:
            return JsonResponse({"error": "Operative was not found"}, status=404)
        json_response = []
        for row in all_rows:
            uniqueactions = row.unique_action.all()
            uniqueactiones = []
            guns = row.gun.all()
            gunes = []
            for gun in guns:
                gunes.append(gun.name)
            for uniqueaction in uniqueactions:
                uniqueactiones.append(uniqueaction.name)
            json_response.append({
                'id': row.pk,
                'name': row.name,
                'stats': {
                    'movement': row.movement,
                    'dash': row.dash,
                    'apl': row.apl,
                    'ga': row.ga,
                    'df': row.df,
                    'sv': row.sv,
                    'w': row.w,
                    'base': row.base,
                },
                'unique_actions': uniqueactiones,
                'guns': gunes,
            })
        return JsonResponse(json_response,safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def gun(request):
    # Manejar la solicitud GET
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("gunName") != None:
            gunName = request.headers.get("gunName")
            try:
                all_rows = Gun.objects.filter(name=gunName)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Gun was not found"}, status=404)
            json_response = []
            for row in all_rows:
                rules = row.special_rule.all()
                ruleses = []
                for rule in rules:
                    ruleses.append(rule.name)
                json_response.append({
                    'id': row.pk,
                    'name': row.name,
                    'stats': {
                        'attacks': row.attacks,
                        'ws': row.ws,
                        'dmg': row.dmg,
                        'critical_dmg': row.dmg,
                    },
                    'rules': ruleses,
                })
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = Gun.objects.all()
            json_response = []
            for row in all_rows:
                json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def gunbyId(request,gunId):
    if request.method == "GET":
        try:
            gun = Gun.objects.get(id=gunId)
        except gun.DoesNotExist:
            return JsonResponse({"error": "Gun was not found"}, status=404)
        rules = gun.special_rule.all()
        ruleses = []
        for rule in rules:
            ruleses.append(rule.name)
        json_response = {
            'id': gun.pk,
            'name': gun.name,
            'stats': {
                'attacks': gun.attacks,
                'ws': gun.ws,
                'dmg': gun.dmg,
                'critical_dmg': gun.dmg,
            },
            'rules': ruleses,
        }
        return JsonResponse(json_response, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def uniqueaction(request):
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("uniqueactionName") != None:
            name = request.headers.get("uniqueactionName")
            try:
                all_rows = UniqueAction.objects.filter(name=name)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Uniqueaction was not found"}, status=404)
            json_response = []
            for row in all_rows:
                json_response.append(row)
        # si no tiene nombre o id en el header devuelve todos
        else:
            all_rows = UniqueAction.objects.all()
            json_response = []
            for row in all_rows:
                json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False)


def uniqueactionbyId(request,uniqueactionId):
    if request.method == "GET":
        try:
            uniqueaction = UniqueAction.objects.get(pk=uniqueactionId)
        except uniqueaction.DoesNotExist:
            return JsonResponse({"error": "Uniqueaction was not found"}, status=404)
        json_response=[]
        json_response.append(uniqueaction)
        return JsonResponse(json_response,safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def specialrule(request):
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("specialruleName") != None:
            specialruleName = request.headers.get("specialruleName")
            try:
                all_rows = SpecialRule.objects.filter(name=specialruleName)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Specialrule was not found"}, status=404)
            json_response = []
            for row in all_rows:
                json_response.append(row)
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = SpecialRule.objects.all()
            json_response = []
            for row in all_rows:
                json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False)


def specialrulebyId(request,specialruleId):
    if request.method == "GET":
        try:
            specialrule = SpecialRule.objects.get(pk=specialruleId)
        except specialrule.DoesNotExist:
            return JsonResponse({"error": "Specialrule was not found"}, status=404)
        json_response = []
        json_response.append(specialrule)
        return JsonResponse(json_response,safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def ability(request):
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("abilityName") != None:
            abilityName = request.headers.get("abilityName")
            try:
                all_rows = Ability.objects.filter(name=abilityName)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Ability was not found"}, status=404)
            json_response = []
            for row in all_rows:
                json_response.append(row)
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = Ability.objects.all()
            json_response = []
            for row in all_rows:
                json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False)


def abilitybyId(request,abilityId):
    if request.method == "GET":
        try:
            ability = Ability.objects.get(pk=abilityId)
        except ability.DoesNotExist:
            return JsonResponse({"error": "Ability was not found"}, status=404)
        json_response = []
        json_response.append(ability)
        JsonResponse(json_response,safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def customarmy(request):
    if request.method == "GET":
        # checkea si tiene nombre en el header y filtrar en caso positivo
        all_rows = CustomArmy.objects.all()
        json_response = []
        for row in all_rows:
            json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False)


@csrf_exempt
def getcustomopp(request): #devuelve todos los custom opps
    if request.method == "GET": #curl -X GET 127.0.0.1:8000/operativegun/
        all_rows = OperativeGun.objects.all()
        json_response = []
        for row in all_rows:
            guns = row.gun.all()
            gunes = []
            opp= ' '
            if row.operative != None:
                opp = row.operative.name
            for gun in guns:
                gunes.append(gun.name)
            json_response.append({
                'id': row.pk,
                'name': row.name,
                'opp_name': opp,
                'guns': gunes,
            })
        return JsonResponse(json_response, safe=False)
    elif request.method=="POST": #curl -X POST --data {\"newOppName\":\"nombre_operative\"} 127.0.0.1:8000/operativegun/
        try:
            # Intentar cargar el JSON del cuerpo de la solicitud
            body_json = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            # Obtener  el nombre de la nueva lista desde el cuerpo del JSON
            json_newOppName = body_json.get('newOppName')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # Crear y guardar una nueva lista de compras
        newcustomopp = OperativeGun()
        newcustomopp.name = json_newOppName.replace("_"," ")
        newcustomopp.save()
        return JsonResponse({"uploaded": True}, status=201)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

@csrf_exempt
def customopp(request,operativegunId): #devuelve un custom opps segun id
    if request.method == "GET":
        row = OperativeGun.objects.get(pk=operativegunId)
        json_response = []
        guns = row.gun.all()
        gunes = []
        opp = ' '
        if row.operative != None:
            opp = row.operative.name
        for gun in guns:
            gunes.append(gun.name)
        json_response.append({
            'id': row.pk,
            'name': row.name,
            'opp_name': opp,
            'guns': gunes,
        })
        return JsonResponse(json_response, safe=False)
    elif request.method == "PUT":
        row = OperativeGun.objects.get(pk=operativegunId)
        try:
            body_json = json.loads(request.body)  # Intentar cargar el JSON del cuerpo de la solicitud
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            oppId = body_json.get('operativeId')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            newname = body_json.get('newName')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            gunId = body_json.get('gunId')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            gunIddel = body_json.get('gunIddel')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # Crear y guardar una nueva lista de compras
        if newname != None:
            row.name = newname.replace("_", " ")
            row.save()
        if oppId != None:
            opp = Operative.objects.get(pk=oppId)
            row.operative=opp
            row.save()
        if gunId != None:
            gun = Gun.objects.get(pk=gunId)
            row.gun.add(gun)
            row.save()
        if gunIddel != None:
            gun = Gun.objects.get(pk=gunIddel)
            row.gun.remove(gun)
            row.save()
        return JsonResponse({"uploaded": True}, status=201)
    elif request.method == "DELETE":
        try:
            opp = OperativeGun.objects.get(pk=operativegunId)
            opp.delete()
            return JsonResponse({'success': True, 'message': 'Operative deleted successfully'}, status=200)
        except OperativeGun.DoesNotExist:
            return JsonResponse({'error': 'Operative not found'}, status=404)

