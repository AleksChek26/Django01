from unittest.mock import patch
from django.test import TestCase
from users.models import CustomUser
from habits.models import Habit

class TaskTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit'
        )

    @patch('habits.tasks.send_telegram_reminder')
    def test_send_telegram_reminder(self, mock_reminder):
        mock_reminder.return_value = True
        # Вызываем функцию или эндпоинт, который её запускает
        result = mock_reminder(self.habit.id)
        self.assertTrue(result)
        mock_reminder.assert_called_once_with(self.habit.id)
