import json

from django.http import JsonResponse

from .models import Operative
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
