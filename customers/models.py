from accounts.models import User
from django.db import models
from invoices.utils import generate_id


class Customer(models.Model):
    id = models.CharField(max_length=12, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Invoice for {self.name}'

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = 'CUS-' + generate_id(8)
        super().save(*args, **kwargs)

    
    class Meta:
        ordering = ('-created_at',)