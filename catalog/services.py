from django.conf import settings
from django.core.mail import send_mail


def send_200views_mail(user):
    send_mail(
        'Просмотры',
        "200 просмотров, ура!!!",
        settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )
