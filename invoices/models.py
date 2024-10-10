from .utils import generate_id
from accounts.models import User
from customers.models import Customer
from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = 'INV-' + generate_id(16)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)


class InvoiceItem(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name} - Quantity: {self.quantity}'

    
    def total_price(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = 'ITEM-' + generate_id(15)
        super().save(*args, **kwargs)


    class Meta:
        ordering = ('-created_at',)
    