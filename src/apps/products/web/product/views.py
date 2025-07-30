# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView
from django.template.loader import render_to_string
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from ...models.product import Product
from apps.core.models.brand import Brand


class ProductTabulatorTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "products/product/tabulator.html"
    login_url = 'users:users_web:web_auth:auth_email_password'

class ProductCatalogTemplateView(ListView):
    model = Product
    template_name = "products/product/catalog.html"
    #login_url = 'users:users_web:web_auth:auth_email_password'
    context_object_name = 'products'
    paginate_by = 5
    ordering = ['-id']

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('p_photos', 'p_prices').order_by('-id')
        search = self.request.GET.get('search')
        brand = self.request.GET.get('brand')

        if search:
            queryset = queryset.filter(Q(code__icontains=search) | Q(description__icontains=search))
        if brand:
            queryset = queryset.filter(brand=brand)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['products'] = products
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            cards_html = render_to_string(
                'products/product/partials/catalog_screen.html', 
                context, 
                request=self.request
            )
            loader_html = render_to_string(
                'products/product/components/catalog_loader.html', 
                context, 
                request=self.request
            )
            return HttpResponse(cards_html + loader_html)
        return super().render_to_response(context, **response_kwargs)

# Funciones htmx
def brand_options(request):
    # Validar que la petición sea HTMX
    if not request.headers.get('HX-Request'):
        return HttpResponseBadRequest("Solo se permiten peticiones HTMX.")

    # Paginación
    #page_number = request.GET.get("page", 1)
    #selected_brand_id = request.GET.get("brand", None)
    qs = Brand.objects.all().order_by("-id")
    #paginator = Paginator(qs, 10)  # 5 opciones por página
    #page_obj = paginator.get_page(page_number)

    # Contexto
    context = {
        "brands": qs,
        #"page_obj": page_obj,
        #"selected_brand_id": selected_brand_id,
    }
    return render(request, "products/product/components/brand_options.html", context)