# Django
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from ...models.product import Product
from django.db.models import Q

def product_tabulator_json(request):
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 10))
    sort_field = request.GET.get('sort', 'code')
    sort_dir = request.GET.get('dir', 'asc')

    qs = Product.objects.filter(is_active=True)

    if search:
        qs = qs.filter(description__icontains=search)

    if sort_field:
        if sort_dir == 'desc':
            sort_field = '-' + sort_field
        qs = qs.order_by(sort_field)

    paginator = Paginator(qs, size)
    page_obj = paginator.get_page(page)

    data = []
    for p in page_obj:
        data.append({
            "id": str(p.id),
            "code": p.code,
            "description": p.description,
            "category": p.category.description_sin if p.category else "",
            "measure": p.measure.name if p.measure else "",
            "brand": p.brand.name if p.brand else "",
            "country": p.country.name if p.country else "",
        })

    return JsonResponse({
        "data": data,
        "last_page": paginator.num_pages,
        "total": paginator.count
    })

class ProductTabulatorTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "products/product/tabulator.html"
    login_url = 'users:users_web:web_auth:auth_email_password'  # URL de inicio de sesión