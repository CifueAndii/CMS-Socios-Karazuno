from django.http import JsonResponse
from .models import EventoPage

def eventos_json(request):
    eventos = EventoPage.objects.live().public().order_by("fecha_inicio")
    data = []
    for evento in eventos:
        data.append({
            "title": evento.title,
            "start": evento.fecha_inicio.isoformat(),
            "end": evento.fecha_fin.isoformat() if evento.fecha_fin else None,
            "location": evento.lugar,
            "url": evento.url,
            "backgroundColor": evento.color,
            "borderColor": evento.color,
        })
    return JsonResponse(data, safe=False)
