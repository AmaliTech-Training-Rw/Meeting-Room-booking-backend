from django.urls import path
from .views import (registration_view, login_view, logout_view,
                    password_reset_view, password_reset_confirm_view)

app_name = "account"
urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('password-reset/confirm/<str:token>/', password_reset_confirm_view, name='password_reset_confirm'),
]
