from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(user):
    subject = 'Підтвердження реєстрації на CompositeEM Lab'
    message = f"Вітаємо, ваш код підтвердження: {user.email_confirmation_code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
