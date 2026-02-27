from django.db import models
from django.core.exceptions import ValidationError

from config import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.TextField()
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    periodicity = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=255, blank=True, null=True)
    execution_time = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def clean(self):
        # Валидация по критериям из ТЗ
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя одновременно указать связанную привычку и вознаграждение.")
        if self.execution_time > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждения или связанной привычки.")
        if self.periodicity > 7:
            raise ValidationError("Периодичность не может быть больше 7 дней.")
