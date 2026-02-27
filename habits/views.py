from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly
from .tasks import send_telegram_reminder



class StandardResultsSetPagination(PageNumberPagination):
    """
    Пагинация с выводом 5 привычек на страницу.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100



class HabitListView(generics.ListAPIView):
    """
    Список привычек текущего пользователя с пагинацией.
    Только для авторизованных пользователей.
    """
    serializer_class = HabitSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_pleasant', 'is_public']

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)



class PublicHabitListView(generics.ListAPIView):
    """
    Список публичных привычек.
    Доступен всем пользователям без аутентификации.
    """
    serializer_class = HabitSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitCreateView(generics.CreateAPIView):
    """
    Создание новой привычки.
    Требует аутентификации.
    После создания запускается задача Celery для напоминания в Telegram.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        # Запускаем задачу Celery для отправки напоминания
        send_telegram_reminder.apply_async(
            args=[habit.id],
            eta=habit.time
        )


class HabitDetailView(generics.RetrieveAPIView):
    """
    Просмотр детальной информации о привычке.
    Доступ только для владельца привычки.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitUpdateView(generics.UpdateAPIView):
    """
    Редактирование привычки.
    Доступ только для владельца привычки.
    При обновлении перезапускается задача напоминания.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        habit = serializer.save()
        # Перезапускаем задачу напоминания с новыми параметрами
        send_telegram_reminder.apply_async(
            args=[habit.id],
            eta=habit.time,
            countdown=0  # Немедленная перезапланировка
        )

class HabitDeleteView(generics.DestroyAPIView):
    """
    Удаление привычки.
    Доступ только для владельца привычки.
    """
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCompleteView(generics.GenericAPIView):
    """
    Отметка выполнения привычки.
    Добавляет запись о выполнении и может запускать бонусные действия.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = HabitSerializer

    def post(self, request, *args, **kwargs):
        habit = self.get_object()
        # Логика отметки выполнения (можно расширить)
        habit.last_completed = timezone.now()
        habit.save()

        # Если есть связанная приятная привычка — предлагаем выполнить
        if habit.related_habit:
            return Response({
                'message': 'Привычка выполнена! Не забудьте выполнить приятную привычку: {}'.format(
                    habit.related_habit.action
        ),
        'related_habit_id': habit.related_habit.id
        }, status=status.HTTP_200_OK)

        return Response({'message': 'Привычка успешно выполнена!'}, status=status.HTTP_200_OK)

    def get_object(self):
        queryset = Habit.objects.filter(user=self.request.user)
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
