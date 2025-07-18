from ...models.product import Product

def get_base_product_tabulator_queryset():
    return Product.objects.filter(is_active=True).select_related(
        "category", "measure", "brand", "country"
    ).prefetch_related("p_prices")