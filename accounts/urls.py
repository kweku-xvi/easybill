from . import views
from django.urls import path


urlpatterns = [
    path('signup', views.signup, name='sign_up'),
    path('verify-user', views.verify_user, name='verify_user'),
    path('login', views.login, name='log_in'),
    path('search', views.search_users, name='search_users'),
    path('user/<str:id>', views.get_user_by_id, name='get_user_by_id'),
    path('all-users', views.get_all_users, name='get_all_users'),
    path('user/update/<str:id>', views.update_user_info, name='update_user'),
    path('user/delete/<str:id>', views.delete_user, name='delete_user'),
    path('password-reset', views.password_reset, name='password_reset'),
    path('password-reset-confirm', views.password_reset_confirm, name='password_reset_confirm'),
]