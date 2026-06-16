# quotations/presentation/admin/__init__.py

from django.contrib import admin
from apps.quotations.infrastructure.persistence.models import Quotation, QuotationItem


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('product', 'quantity', 'unit_price', 'subtotal')


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'expired','notification_sent', 'total', 'currency_code', 'status')
    list_filter = ('status', 'currency_code', 'created')
    search_fields = ('id', 'user__email')
    readonly_fields = ('id', 'created', 'subtotal', 'total')
    inlines = [QuotationItemInline]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('id', 'user', 'status')
        }),
        ('Fechas', {
            'fields': ('created', 'expired')
        }),
        ('Precios', {
            'fields': ('profit_margin', 'currency_code', 'subtotal', 'total')
        }),
        ('Contacto', {
            'fields': ('whatsapp',)
        }),
    )


@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'quotation', 'get_product_description', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('quotation__status',)
    search_fields = ('quotation__id', 'product__code', 'product__description')
    readonly_fields = ('subtotal',)
    
    def get_product_description(self, obj):
        return obj.product.description
    get_product_description.short_description = 'Product'