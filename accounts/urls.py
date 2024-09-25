from . import views
from django.urls import path


urlpatterns = [
    path('signup', views.signup, name='sign_up'),
    path('verify-user', views.verify_user, name='verify_user'),
    path('login', views.login, name="log_in"),
]