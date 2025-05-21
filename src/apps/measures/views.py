# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
# Models
from .models import Measure

def hx_measure_card_list(request):
    search = request.GET.get("search", "")
    page = request.GET.get('page', 1)
    objs = Measure.objects.filter(name__icontains=search).order_by("name")
    paginator = Paginator(objs, 5) # 5 categorías por página
    context = {
        'objs': paginator.get_page(page),
        "search": search,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'measures/partials/card-list.html', context)
    return render(request, 'measures/main.html', context)

def hx_measure_detail(request, pk):
    obj = get_object_or_404(Measure, pk=pk)
    context = {
        "obj": obj,
    }
    # Solo devuelves el detalle como fragmento
    if request.headers.get('HX-Request'):
        return render(request, 'measures/modals/detail.html', context)
    else:
        # Redirige a una vista principal, puedes pasar el contexto si necesitas
        return redirect('measures:hx_measure_card_list')



