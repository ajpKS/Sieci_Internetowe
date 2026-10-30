from django.http import JsonResponse
from django.shortcuts import render

from .models import Gra


def strona_glowna(request):
    return render(request, 'gry/index.html', {'gatunki': Gra.GATUNKI})


def api_gry(request):
    gry = Gra.objects.all()

    wieloosobowa = request.GET.get('wieloosobowa')
    if wieloosobowa in ('true', 'false'):
        gry = gry.filter(wieloosobowa=(wieloosobowa == 'true'))

    gatunek = request.GET.get('gatunek')
    if gatunek in dict(Gra.GATUNKI):
        gry = gry.filter(gatunek=gatunek)

    items = [
        {
            'id': g.id,
            'tytul': g.tytul,
            'opis': g.opis,
            'gatunek': g.get_gatunek_display(),
            'data_premiery': g.data_premiery.isoformat(),
            'ocena': g.ocena,
            'wieloosobowa': g.wieloosobowa,
            'cena': float(g.cena),
        }
        for g in gry
    ]
    return JsonResponse({'items': items})
