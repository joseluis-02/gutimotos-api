# Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
# Models
from .models import Category

"""
class CategoryListView(View):
    def get(self, request):
        search = request.GET.get("search", "")
        page_number = request.GET.get("page", 1)

        categories = Category.objects.filter(name__icontains=search).order_by("name")
        paginator = Paginator(categories, 10)

        context = {
            "page_obj": paginator.get_page(page_number),
            "search": search,
        }
        if request.headers.get('HX-Request'):
            return render(request, 'categories/includes/table.html', context)
        return render(request, 'categories/main.html', context)
class CategoryDetailView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)

        context = {
            "category": category,
        }
        # Solo devuelves el detalle como fragmento
        if request.headers.get('HX-Request'):
            return render(request, 'categories/includes/detail.html', context)
        else:
            # Redirige a una vista principal, puedes pasar el contexto si necesitas
            return redirect('categories:category_list')
"""
def hx_category_card_list(request):
    search = request.GET.get("search", "")
    page = request.GET.get('page', 1)
    objs = Category.objects.filter(description_sin__icontains=search).order_by("description_sin")
    paginator = Paginator(objs, 5) # 5 categorías por página
    context = {
        'objs': paginator.get_page(page),
        "search": search,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'categories/partials/card-list.html', context)
    return render(request, 'categories/main.html', context)





def hx_category_list_table(request):
    search = request.GET.get("search", "")
    page_number = request.GET.get("page", 1)

    categories = Category.objects.filter(name__icontains=search).order_by("name")
    paginator = Paginator(categories, 10)

    context = {
        "page_obj": paginator.get_page(page_number),
        "search": search,
    }
    if request.headers.get('HX-Request'):
        # Respuesta parcial (HTMX)
        return render(request, 'categories/includes/table.html', context)
    else:
        # Redirige a una vista principal, puedes pasar el contexto si necesitas
        return redirect('categories:hx_category_card_list')
def hx_category_detail(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    context = {
        "obj": obj,
    }
    # Solo devuelves el detalle como fragmento
    if request.headers.get('HX-Request'):
        return render(request, 'categories/modals/detail.html', context)
    else:
        # Redirige a una vista principal, puedes pasar el contexto si necesitas
        return redirect('categories:hx_category_card_list')



