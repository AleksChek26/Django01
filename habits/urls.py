from django.urls import path
from . import views

urlpatterns = [
    # Список привычек пользователя с пагинацией (5 на страницу)
    path(
        'habits/',
        views.HabitListView.as_view(),
        name='habit-list'
    ),

    # Создание новой привычки
    path(
        'habits/create/',
        views.HabitCreateView.as_view(),
        name='habit-create'
    ),

    # Детальная информация о привычке
    path(
        'habits/<int:pk>/',
        views.HabitDetailView.as_view(),
        name='habit-detail'
    ),

    # Обновление привычки
    path(
        'habits/<int:pk>/update/',
        views.HabitUpdateView.as_view(),
        name='habit-update'
    ),

    # Удаление привычки
    path(
        'habits/<int:pk>/delete/',
        views.HabitDeleteView.as_view(),
        name='habit-delete'
    ),

    # Отметка выполнения привычки
    path(
        'habits/<int:pk>/complete/',
        views.HabitCompleteView.as_view(),
        name='habit-complete'
    ),

    # Список публичных привычек (доступен всем)
    path(
        'public-habits/',
        views.PublicHabitListView.as_view(),
        name='public-habit-list'
    ),
]
