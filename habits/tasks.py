from celery import shared_task
import telegram
from .models import Habit

@shared_task
def send_telegram_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
    bot.send_message(chat_id=habit.user.telegram_chat_id, text=message)
