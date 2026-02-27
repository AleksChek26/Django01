from django.test import TestCase, Client
from users.models import CustomUser
from habits.models import Habit
from rest_framework.authtoken.models import Token

class HabitViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = Client()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_habit(self):
        response = self.client.post('/api/habits/create/', {
            'name': 'Test Habit',
            'is_pleasant': True
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_habit_list(self):
        Habit.objects.create(user=self.user, name='Habit 1')
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
