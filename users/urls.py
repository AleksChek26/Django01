from django.urls import path
from . import views

urlpatterns = [
    # Регистрация нового пользователя
    path(
        'register/',
        views.register,
        name='user-register'
    ),

    # Аутентификация (получение токена)
    path(
        'login/',
        views.login_user,
        name='user-login'
    ),

    # Выход из системы
    path(
        'logout/',
        views.logout_user,
        name='user-logout'
    ),

    # Получение и обновление профиля текущего пользователя
    path(
        'profile/',
        views.user_profile,
        name='user-profile'
    ),
]
