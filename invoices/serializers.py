from .models import Invoice, InvoiceItem
from rest_framework import serializers


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'invoice_date', 'sub_total', 'sender']

        read_only_fields = ['id', 'invoice_date', 'customer', 'sender']


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'name', 'quantity', 'unit_price', 'invoice']

        read_only_fields = ['id', 'invoice']