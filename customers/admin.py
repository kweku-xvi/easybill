from .models import Customer
from django.contrib import admin

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number')
    readonly_fields = ('created_at',)


admin.site.register(Customer, CustomerAdmin)