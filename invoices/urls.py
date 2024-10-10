from . import views
from django.urls import path


urlpatterns = [
    path('all', views.get_invoices_by_user, name='get_user_invoices'),
    path('create/<str:customer_id>', views.create_invoice, name='create_invoice'),
    path('add-item/<str:invoice_id>', views.add_item_to_invoice, name='add_item'),
    path('get-all-items/<str:invoice_id>', views.get_invoice_items, name='get_items_in_invoice'),
    path('update-item/<str:item_id>', views.update_invoice_item, name='update_item'),
    path('remove-item/<str:item_id>', views.remove_invoice_item, name='remove_item'),
    path('delete/<str:invoice_id>', views.delete_invoice, name='delete_invoice'),
]