import json

from django.http import JsonResponse
from .models import Operative, Gun, SpecialRule
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
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
                json_response.append(row.to_json())
        # si no tiene nombre en el header devuelve todos
        elif request.headers.get("operativeId") != None:
            operativeId = request.headers.get("operativeId")
            try:
                all_rows = Operative.objects.filter(name=operativeId)
            except all_rows.DoesNotExist:
                return JsonResponse({"error": "Operative was not found"}, status=404)
            json_response = []
            for row in all_rows:
                json_response.append(row.to_json())
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = Operative.objects.all()
            json_response = []
            for row in all_rows:
                json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False)
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
        elif request.headers.get("gunId") != None:
            gunId = request.headers.get("gunId")
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
        # si no tiene nombre en el header devuelve todos
        else:
            all_rows = Gun.objects.all()
            json_response = []
            for row in all_rows:
                json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


def JSONLIADA(request, json_response=None, self=None):
    # rule = SpecialRule.objects.get(id=1)
    # Add the gun to the rule
    # gun.special_rule.add(rule)
    # gun.save()
    return JsonResponse