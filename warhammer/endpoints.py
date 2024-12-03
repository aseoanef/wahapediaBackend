import random
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Operative, Gun, SpecialRule, UniqueAction, Ability , Army, CustomArmy, OperativeGun
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
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
                operativeses = [] #lista de operativos
                abilitys = row.ability.all()
                abilityses = [] #lista de abilidades
                for operative in operatives:
                    operativeses.append(operative.name)
                for ability in abilitys:
                    abilityses.append(ability.name)
                json_response.append({ #añadir los datos a la respuesta
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
                operativeses = [] #lista de soldados
                abilitys = row.ability.all()
                abilityses = [] #lista de habilidades
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
    elif request.method == "POST": #curl -X POST --data {\"name\":\"Hunter_Clade\",\"faction\":\"Adeptus_mechanicus\"} http://127.0.0.1:8000/army/
        try:
            body_json = json.loads(request.body)
            name = body_json.get('name').replace("_"," ")
            faction = body_json.get('faction').replace("_"," ")
            if not name or not faction:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            try:
                new_army = Army(name=name,faction=faction) #crear un nuevo ejército
                new_army.save()
                return JsonResponse({'success': True, 'army': new_army.to_json()}, status=201)
            except IntegrityError:
                return JsonResponse({'error':'Army with this name already exists'},status=409)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def armybyId(request,armyId):
    # Manejar la solicitud GET
    if request.method == 'GET':
        try:
            all_rows = Army.objects.get(pk=armyId)
        except all_rows.DoesNotExist:
            return JsonResponse({"error": "Army was not found"}, status=404)
        json_response = []
        operatives = all_rows.operatives.all()
        operativeses = [] #lista de los soldados
        abilitys = all_rows.ability.all()
        abilityses = [] #lista de las habilidades
        for operative in operatives:
            operativeses.append(operative.name) #rellenar la lista de soldados
        for ability in abilitys:
            abilityses.append(ability.name) #rellenar la lista de habilidades
        json_response.append({ #rellenar la respuesta con el ejército
            'id': all_rows.pk,
            'name': all_rows.name,
            'faction': all_rows.faction,
            'operatives': operativeses,
            'abilities': abilityses,
        })
        return JsonResponse(json_response, safe=False)
    elif request.method == "PUT":  #curl -X PUT --data {\"operativeId\":2,\"abilityId\":2} http://127.0.0.1:8000/army/2/
        row = Army.objects.get(pk=armyId)
        try:
            body_json = json.loads(request.body)  #Intentar cargar el JSON del cuerpo de la solicitud
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            oppId = body_json.get('operativeId') #Checkear si la solicitud incluye la id de un soldado
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            abilityId = body_json.get('abilityId') #Checkear si la solicitud incluye la id de una abilidad
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # guardar los datos en la army
        if oppId != None: #si la solicitud incluye la id de un soldados, añadirlo al ejército
            opp = Operative.objects.get(pk=oppId)
            row.operatives.add(opp)
            row.save()
        if abilityId != None: #si la solicitud incluye la id de una abilidad, añadirla al ejército
            ability = Ability.objects.get(pk=abilityId)
            row.ability.add(ability)
            row.save()
        return JsonResponse({"uploaded": True}, status=201)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def operative(request):
    # Manejar la solicitud GET
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("operativeName") != None:
            operativeName = request.headers.get("operativeName") #sacar el nombre de el soldado de los headers
            try:
                all_rows = Operative.objects.filter(name=operativeName)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Operative was not found"}, status=404)
            json_response = []
            for row in all_rows:
                uniqueactions = row.unique_action.all() #sacar todas las acciones unicas del soldado
                uniqueactiones = []
                guns = row.gun.all() #sacar todas las armas de el soldado
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
    elif request.method == "POST":  #curl -X POST --data {\"name\":\"Skitarii_Ranger_Marksman\",\"movement\":3,\"dash\":2,\"apl\":2,\"ga\":1,\"df\":3,\"sv\":4,\"w\":7,\"base\":25} http://127.0.0.1:8000/operative/
        try:
            body_json = json.loads(request.body)
            name = body_json.get('name').replace("_", " ")
            movement = body_json.get('movement') #movement
            dash = body_json.get('dash') #dash
            apl = body_json.get('apl') #action points limit
            ga = body_json.get('ga') #group actions
            df = body_json.get('df') #defence
            sv = body_json.get('sv') #save throw
            w = body_json.get('w') #wounds
            base = body_json.get('base') #base diámetro
            if not name or not movement or not dash or not apl or not ga or not df or not sv or not w or not base:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            new_opp = Operative(name=name, movement=movement, dash=dash, apl=apl, ga=ga, df=df, sv=sv, w=w, base=base)
            new_opp.save()
            return JsonResponse({'success': True, 'operative': new_opp.to_json()}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def operativebyId(request,operativeId):
    if request.method == "GET":
        try:
            all_rows = Operative.objects.get(pk=operativeId)
        except all_rows.DoesNotExist:
            return JsonResponse({"error": "Operative was not found"}, status=404)
        json_response = []
        uniqueactions = all_rows.unique_action.all()
        uniqueactiones = [] #lista de acciones únicas
        guns = all_rows.gun.all()
        gunes = []
        for gun in guns:
            gunes.append(gun.name)
        for uniqueaction in uniqueactions:
            uniqueactiones.append(uniqueaction.name)
        json_response.append({
            'id': all_rows.pk,
            'name': all_rows.name,
            'stats': {
                'movement': all_rows.movement,
                'dash': all_rows.dash,
                'apl': all_rows.apl,
                'ga': all_rows.ga,
                'df': all_rows.df,
                'sv': all_rows.sv,
                'w': all_rows.w,
                'base': all_rows.base,
            },
            'unique_actions': uniqueactiones,
            'guns': gunes,
        })
        return JsonResponse(json_response,safe=False)
    elif request.method == "PUT": #curl -X PUT --data {\"gunId\":3,\"uniqueactionId\":2} http://127.0.0.1:8000/operative/2/
        row = Operative.objects.get(pk=operativeId)
        try:
            body_json = json.loads(request.body)  # Intentar cargar el JSON del cuerpo de la solicitud
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            gunId = body_json.get('gunId')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            uniqueactionId = body_json.get('uniqueactionId')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # guardar los datos en el operative
        if uniqueactionId != None:
            uniqueaction = UniqueAction.objects.get(pk=uniqueactionId) #sacar la acción única de el soldado
            row.unique_action.add(uniqueaction)
            row.save()
        if gunId != None:
            gun = Gun.objects.get(pk=gunId) #sacar el arma de el soldado
            row.gun.add(gun)
            row.save()
        return JsonResponse({"uploaded": True}, status=201)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def gun(request):
    # Manejar la solicitud GET
    if request.method == 'GET':
        # checkea si tiene nombre en el header y filtrar en caso positivo
        if request.headers.get("gunName") != None:
            gunName = request.headers.get("gunName") #sacar el nombre del arma si hay
            try:
                all_rows = Gun.objects.filter(name=gunName)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Gun was not found"}, status=404)
            json_response = []
            for row in all_rows:
                rules = row.special_rule.all()
                ruleses = [] #lista de reglas en el arma
                for rule in rules:
                    ruleses.append(rule.name) #añadir cada regla especial a la lista
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
                json_response.append(row.to_json()) #añadir todas las armas a la respuesta
        return JsonResponse(json_response, safe=False)
    elif request.method == "POST":  #curl -X POST --data {\"name\":\"Galvanic_rifle\",\"attacks\":4,\"ws\":3,\"dmg\":3,\"critical_dmg\":4} http://127.0.0.1:8000/gun/
        try:
            body_json = json.loads(request.body)
            name = body_json.get('name').replace("_", " ")
            attacks = body_json.get('attacks')
            ws = body_json.get('ws')
            dmg = body_json.get('dmg')
            critical_dmg =body_json.get('critical_dmg')
            if not name or not attacks or not ws or not dmg or not critical_dmg: #nombre, ataques, ws, dmg, critical_dmg son obligatorios
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            new_gun = Gun(name=name, attacks=attacks, ws=ws , dmg=dmg, critical_dmg=critical_dmg) #crear la nuevo arma
            new_gun.save()
            return JsonResponse({'success': True, 'gun': new_gun.to_json()}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
# Función para manejar solicitudes GET y PUT para un objeto Gun por su ID
def gunbyId(request,gunId):
    # Manejar solicitud GET para obtener detalles del Gun
    if request.method == "GET":
        try:
            # Intentar obtener el objeto Gun por su ID
            gun = Gun.objects.get(id=gunId)
        except gun.DoesNotExist:
            # Si el Gun no existe, devolver una respuesta de error 404
            return JsonResponse({"error": "Gun was not found"}, status=404)
        # Obtener todas las reglas especiales relacionadas con el Gun
        rules = gun.special_rule.all()
        ruleses = []
        for rule in rules:
            # Añadir el nombre de cada regla a la lista ruleses
            ruleses.append(rule.name)
        # Crear respuesta JSON con detalles del Gun
        json_response = {
            'id': gun.pk,
            'name': gun.name,
            'stats': {
                'attacks': gun.attacks,
                'ws': gun.ws,
                'dmg': gun.dmg,
                'critical_dmg': gun.dmg, # Podría ser un error tipográfico, ¿debería ser gun.critical_dmg?
            },
            'rules': ruleses,
        }
        # Devolver la respuesta JSON
        return JsonResponse(json_response, safe=False)
    # Manejar solicitud PUT para actualizar detalles del Gun
    elif request.method == "PUT": #curl -X PUT --data {\"specialruleId\":3} http://127.0.0.1:8000/gun/3/
        row = Gun.objects.get(pk=gunId)
        try:
            # Cargar el cuerpo JSON de la solicitud
            body_json = json.loads(request.body)  # Intentar cargar el JSON del cuerpo de la solicitud
        except json.JSONDecodeError:
            # Devolver una respuesta de error 400 si el JSON es inválido
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            # Obtener el specialruleId del cuerpo JSON
            specialruleId = body_json.get('specialruleId')
        except KeyError:
            # Devolver una respuesta de error 400 si falta specialruleId
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # Añadir la regla especial al Gun si se proporciona specialruleId
        if specialruleId != None:
            specialrule = SpecialRule.objects.get(pk=specialruleId)
            row.special_rule.add(specialrule)
            row.save()
        # Devolver una respuesta 201 indicando éxito
        return JsonResponse({"uploaded": True}, status=201)
    # Devolver una respuesta de error 405 para métodos HTTP no soportados
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


# Metodo para simular un ataque de un arma por su ID
def attack(request,gunId):#metodo para simular un ataque de un arma por id
    if request.method == "GET":
        try:
            # Intentar obtener el objeto Gun por su ID
            gun = Gun.objects.get(id=gunId)
        except gun.DoesNotExist:
            # Si el Gun no existe, devolver una respuesta de error 404
            return JsonResponse({"error": "Gun was not found"}, status=404)
        # Obtener todas las reglas especiales relacionadas con el Gun
        rules = gun.special_rule.all()
        ruleses = []
        dices=[]
        potentialdmg=0
        # Hacemos un loop para tirar los dados por cada ataque
        for x in range(gun.attacks):
            roll=random.randint(1,6)#simulamos la tirada de 1d6 (un dado de 6 caras)
            if roll >= gun.ws: #comprobamos si da el ataque
                if roll == 6: #si es crítico
                    potentialdmg+=gun.critical_dmg #sumamos el daño de critico
                potentialdmg+=gun.dmg #sumamos el daño de critico
            dices.append(roll) #guardamos todos los dados por si alguna habilidad se activa aunque falle el ataque
        for rule in rules:
            ruleses.append(rule.name) #añadimos todas las reglas que competen para facil acceso
        # Fabricamos la respuesta JSON
        json_response = {
            'name': gun.name,
            'result': {
                'attacks': dices,
                'max_dmg':potentialdmg,
            },
            'stats':{
                'ws/bs':gun.ws,
                'dmg': gun.dmg,
                'critical_dmg': gun.critical_dmg,
            },
            'rules': ruleses,
        }
        # Devolver la respuesta JSON
        return JsonResponse(json_response, safe=False)
    else:
        # Devolver una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
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
    elif request.method == "POST":  #curl -X POST --data {\"name\":\"Omnispex\",\"description\":\"Select_one_friendly_HUNTER_CLADE_operative_Visible_to_and_within_of_this_operative,_then_select_one_enemy_operative._Until_the_end_of_the_Turning_Point,_each_time_that_friendly_operative_makes_a_shooting_attack,_for_that_shooting_attack:_Areas_of_smoke_have_no_effect_when_determining_Line_of_Sight_to_that_enemy_operative._That_enemy_operative_is_not_Obscured._If_that_enemy_operative_is_the_target,_that_friendly_operative’s_ranged_weapons_have_the_No_Cover_special_rule._This_operative_cannot_perform_this_action_while_within_Engagement_Range_of_an_enemy_operative.\",\"cost\":1} http://127.0.0.1:8000/uniqueaction/
        try:
            body_json = json.loads(request.body)
            name = body_json.get('name').replace("_", " ")
            description = body_json.get('description').replace("_", " ")
            cost = body_json.get('cost')
            if not name or not description:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            new_unique_action = UniqueAction(name=name, description=description)
            if cost != None:
                new_unique_action.cost = cost
            new_unique_action.save()
            return JsonResponse({'success': True, 'unique_action': new_unique_action.to_json()}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


# Función para manejar solicitudes para una UniqueAction por su ID
def uniqueactionbyId(request,uniqueactionId):
    if request.method == "GET":
        try:
            # Intentar obtener el objeto UniqueAction por su ID
            uniqueaction = UniqueAction.objects.get(pk=uniqueactionId)
        except uniqueaction.DoesNotExist:
            # Si la UniqueAction no existe, devolver una respuesta de error 404
            return JsonResponse({"error": "Uniqueaction was not found"}, status=404)
        # Crear una lista para la respuesta JSON
        json_response=[]
        # Añadir el resultado de la conversión a JSON de la UniqueAction a la lista
        json_response.append(uniqueaction.to_json())
        # Devolver la respuesta JSON
        return JsonResponse(json_response,safe=False)
    else:
        # Devolver una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def specialrule(request):
    if request.method == 'GET':
        # Verifica si hay un nombre en el header y filtra en caso positivo
        if request.headers.get("specialruleName") != None:
            specialruleName = request.headers.get("specialruleName")
            try:
                # Filtra las reglas especiales por nombre
                all_rows = SpecialRule.objects.filter(name=specialruleName)
            except all_rows.DoesNotExist:
                # Si no se encuentra la regla especial, devuelve un error 404
                return JsonResponse({"error": "Specialrule was not found"}, status=404)
            json_response = []
            for row in all_rows:
                # Añade cada fila al JSON de respuesta
                json_response.append(row)
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = SpecialRule.objects.all()
            json_response = []
            for row in all_rows:
                # Convierte cada fila a JSON y añádela a la respuesta
                json_response.append(row.to_json())
        # Devuelve la respuesta JSON
        return JsonResponse(json_response, safe=False)
    elif request.method == "POST": # curl -X POST --data {\"name\":\"stun\",\"description\":\"stunea_neno\",\"modifier\":2} http://127.0.0.1:8000/specialrule/
        try:
            # Intenta cargar el JSON del cuerpo de la solicitud
            body_json = json.loads(request.body)
            name = body_json.get('name')
            description = body_json.get('description').replace("_"," ")
            modifier = body_json.get('modifier')
            # Verifica si se proporcionan los campos requeridos
            if not name or not description:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            # Crea una nueva regla especial con los datos proporcionados
            new_special_rule = SpecialRule(name=name,description=description)
            if modifier != None:
                new_special_rule.modifier=modifier
            new_special_rule.save()
            # Devuelve una respuesta de éxito con la nueva regla
            return JsonResponse({'success': True, 'rule': new_special_rule.to_json()}, status=201)
        except json.JSONDecodeError:
            # Devuelve un error 400 si el JSON es inválido
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        # Devuelve un error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


# Función para manejar solicitudes para una SpecialRule por su ID
def specialrulebyId(request,specialruleId):
    if request.method == "GET":
        try:
            # Intentar obtener el objeto SpecialRule por su ID
            specialrule = SpecialRule.objects.get(pk=specialruleId)
        except specialrule.DoesNotExist:
            # Si la SpecialRule no existe, devolver una respuesta de error 404
            return JsonResponse({"error": "Specialrule was not found"}, status=404)
        # Crear una lista para la respuesta JSON
        json_response = []
        # Añadir el objeto SpecialRule a la lista
        json_response.append(specialrule)
        # Devolver la respuesta JSON
        return JsonResponse(json_response,safe=False)
    else:
        # Devolver una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def ability(request):
    if request.method == 'GET':
        # Verifica si hay un nombre en el header y filtra en caso positivo
        if request.headers.get("abilityName") != None:
            abilityName = request.headers.get("abilityName")
            try:
                # Filtra las habilidades por nombre
                all_rows = Ability.objects.filter(name=abilityName)
            except all_rows.DoesNotExist:
                # Si no se encuentra la habilidad, devuelve un error 404
                return JsonResponse({"error": "Ability was not found"}, status=404)
            json_response = []
            for row in all_rows:
                # Añade cada fila al JSON de respuesta
                json_response.append(row)
        # Si no hay nombre en el header, devuelve todas las habilidades
        else:
            all_rows = Ability.objects.all()
            json_response = []
            for row in all_rows:
                # Convierte cada fila a JSON y la añade a la respuesta
                json_response.append(row.to_json())
        # Devuelve la respuesta JSON
        return JsonResponse(json_response, safe=False)
    elif request.method == "POST":  #curl -X POST --data {\"name\":\"Conqueror_Imperative\",\"description\":\"Optimisation:_Each_time_a_friendly_HUNTER_CLADE_operative_fights_in_combat,_in_the_Roll_Attack_Dice_step_of_that_combat,_you_can_re-roll_one_of_your_attack_dice.\",\"cost\":2} http://127.0.0.1:8000/ability/
        try:
            # Intenta cargar el JSON del cuerpo de la solicitud
            body_json = json.loads(request.body)
            name = body_json.get('name').replace("_", " ")
            description = body_json.get('description').replace("_", " ")
            cost = body_json.get('cost')
            # Verifica si se proporcionan los campos requeridos
            if not name or not description:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            # Crea una nueva habilidad con los datos proporcionados
            new_ability = Ability(name=name, description=description)
            if cost != None:
                new_ability.cost = cost
            new_ability.save()
            # Devuelve una respuesta de éxito con la nueva habilidad
            return JsonResponse({'success': True, 'ability': new_ability.to_json()}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        # Devuelve un error 400 si el JSON es inválido
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


# Función para manejar solicitudes para una Ability por su ID
def abilitybyId(request,abilityId):
    if request.method == "GET":
        try:
            # Intentar obtener el objeto Ability por su ID
            ability = Ability.objects.get(pk=abilityId)
        except ability.DoesNotExist:
            # Si la Ability no existe, devolver una respuesta de error 404
            return JsonResponse({"error": "Ability was not found"}, status=404)
        # Crear una lista para la respuesta JSON
        json_response = []
        # Añadir el resultado de la conversión a JSON de la Ability a la lista
        json_response.append(ability.to_json())
        # Devolver la respuesta JSON
        return JsonResponse(json_response,safe=False)
    else:
        # Devolver una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def getcustomarmy(request): #devuelve todos los custom opps
    if request.method == "GET": #curl -X GET 127.0.0.1:8000/customarmy/
        all_rows = CustomArmy.objects.all() # Obtiene todas las filas de CustomArmy
        json_response = []
        for row in all_rows:
            operative = row.operative.all() # Obtiene todos los operativos relacionados con cada fila de CustomArmy
            result={}
            for operativ in operative:
                result={
                    "id":operativ.id,
                    "name":operativ.name,
                }
            json_response.append({
                'id': row.pk,
                'name': row.name,
                'operatives': result,
            })
        return JsonResponse(json_response, safe=False)
    elif request.method=="POST": #curl -X POST --data {\"newArmyName\":\"nombre_army\"} 127.0.0.1:8000/customarmy/
        try:
            # Intentar cargar el JSON del cuerpo de la solicitud
            body_json = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            # Obtener el nombre del nuevo ejército desde el cuerpo del JSON
            json_newArmyName = body_json.get('newArmyName')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # Crear y guardar una nueva lista de compras
        army = CustomArmy()
        army.name = json_newArmyName.replace("_"," ")
        army.save()
        return JsonResponse({"uploaded": True}, status=201)
    else:
        # Devolver una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def customarmy(request,customarmyId): # devuelve un custom opps según id
    if request.method == "GET":
        # Obtener el objeto CustomArmy por su ID
        row = CustomArmy.objects.get(pk=customarmyId)
        json_response = []
        # Obtener todos los operativos relacionados con el CustomArmy
        operatives= row.operative.all()
        listoperatives = {}
        # Añadir el CustomArmy y sus operativos a la respuesta JSON
        for operative in operatives:
            listoperatives={
                "id":operative.id,
                "name":operative.name,
            }
        json_response.append({
            'id': row.pk,
            'name': row.name,
            'operatives': listoperatives,
        })
        return JsonResponse(json_response, safe=False)
    elif request.method == "PUT":
        # Obtener el objeto CustomArmy por su ID
        army = CustomArmy.objects.get(pk=customarmyId)
        try:
            # Intentar cargar el JSON del cuerpo de la solicitud
            body_json = json.loads(request.body) # Intentar cargar el JSON del cuerpo de la solicitud
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            # Obtener el ID del operativo desde el JSON del cuerpo de la solicitud
            oppId = body_json.get('operativeId')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            newname = body_json.get('newName')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # Actualizar y guardar el nombre del CustomArmy si se proporciona
        if newname != None:
            army.name = newname.replace("_"," ")
            army.save()
        # Añadir un nuevo operativo al CustomArmy si se proporciona
        if oppId != None:
            operative = OperativeGun.objects.get(pk=oppId)
            army.operative.add(operative)
            army.save()
        return JsonResponse({"uploaded": True}, status=201)
    elif request.method == "DELETE":
        try:
            # Obtener y eliminar el objeto CustomArmy por su ID
            army = CustomArmy.objects.get(pk=customarmyId)
            army.delete()
            return JsonResponse({'success': True, 'message': 'Army deleted successfully'}, status=200)
        except CustomArmy.DoesNotExist:
            return JsonResponse({'error':'Army not found'}, status=404)
    else:
        # Devolver una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def getcustomopp(request): #devuelve todos los custom opps
    if request.method == "GET": #curl -X GET 127.0.0.1:8000/operativegun/
        all_rows = OperativeGun.objects.all() () # Obtiene todas las filas de OperativeGun
        json_response = []
        for row in all_rows:
            guns = row.gun.all() # Obtiene todas las armas relacionadas con cada fila de OperativeGun
            gunes = []
            opp= ' '
            if row.operative != None:
                opp = row.operative.name # Obtiene el nombre del operativo si existe
            for gun in guns:
                gunes.append(gun.name) # Añade el nombre de cada arma a la lista gunes
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
        # Devuelve una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


@csrf_exempt
def customopp(request,operativegunId): #devuelve un custom opps segun id
    if request.method == "GET":
        # Obtener el objeto OperativeGun por su ID
        row = OperativeGun.objects.get(pk=operativegunId)
        json_response = []
        # Obtener todas las armas relacionadas con el OperativeGun
        guns = row.gun.all()
        gunes = []
        opp = ' '
        if row.operative != None:
            opp = row.operative.name # Obtener el nombre del operativo si existe
        for gun in guns:
            gunes.append(gun.name) # Añadir el nombre de cada arma a la lista gunes
        # Añadir el OperativeGun y sus armas a la respuesta JSON
        json_response.append({
            'id': row.pk,
            'name': row.name,
            'opp_name': opp,
            'guns': gunes,
        })
        return JsonResponse(json_response, safe=False)
    elif request.method == "PUT": #curl -X PUT --data {\"operativeId\":2,\"gunId\":2} 127.0.0.1:8000/operativegun/1/
        row = OperativeGun.objects.get(pk=operativegunId)
        # Intentar cargar el JSON del cuerpo de la solicitud
        try:
            body_json = json.loads(request.body)  # Intentar cargar el JSON del cuerpo de la solicitud
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            # Obtener el ID del operativo desde el JSON del cuerpo de la solicitud
            oppId = body_json.get('operativeId')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            # Obtener el nuevo nombre desde el JSON del cuerpo de la solicitud
            newname = body_json.get('newName')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            # Obtener el ID del arma desde el JSON del cuerpo de la solicitud
            gunId = body_json.get('gunId')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        try:
            # Obtener el ID del arma a eliminar desde el JSON del cuerpo de la solicitud
            gunIddel = body_json.get('gunIddel')
        except KeyError:
            return JsonResponse({"error": "Missing parameter in request"}, status=400)
        # Actualizar y guardar el nombre del OperativeGun si se proporciona
        if newname != None:
            row.name = newname.replace("_", " ")
            row.save()
        # Actualizar el operativo del OperativeGun si se proporciona
        if oppId != None:
            opp = Operative.objects.get(pk=oppId)
            row.operative=opp
            row.save()
        # Añadir un arma al OperativeGun si se proporciona
        if gunId != None:
            gun = Gun.objects.get(pk=gunId)
            row.gun.add(gun)
            row.save()
        # Eliminar un arma del OperativeGun si se proporciona
        if gunIddel != None:
            gun = Gun.objects.get(pk=gunIddel)
            row.gun.remove(gun)
            row.save()
        return JsonResponse({"uploaded": True}, status=201)
    elif request.method == "DELETE":
        try:
            # Obtener y eliminar el objeto OperativeGun por su ID
            opp = OperativeGun.objects.get(pk=operativegunId)
            opp.delete()
            return JsonResponse({'success': True, 'message': 'Operative deleted successfully'}, status=200)
        except OperativeGun.DoesNotExist:
            return JsonResponse({'error': 'Operative not found'}, status=404)
    else:
    # Devolver una respuesta de error 405 para métodos HTTP no soportados
        return JsonResponse({'error': 'Método HTTP no soportado'},status=405)
