from django.test import TestCase
from users.models import CustomUser
from habits.models import Habit

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            is_pleasant=True
        )
        self.assertEqual(habit.name, 'Test Habit')
