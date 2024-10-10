from .models import Invoice, InvoiceItem
from django.contrib import admin

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'sub_total', 'sender')
    readonly_fields = ('created_at',)


class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'unit_price', 'invoice')
    readonly_fields = ('created_at',)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)