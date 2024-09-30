from . import views
from django.urls import path

urlpatterns = [
    path('add', views.add_customer, name='add_customer'),
    path('all', views.get_all_customers, name='get_all_customers'),
    path('<str:id>', views.get_customer_by_id, name='get_customer_by_id'),
    path('update/<str:id>', views.update_customer_info, name='update_customer'),
    path('delete/<str:id>', views.delete_customer, name='delete_customer'),
]