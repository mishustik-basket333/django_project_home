from django import template
from django.core.mail import send_mail

from config import settings

register = template.Library()
@register.simple_tag
def verification(user):

    send_mail(
        subject="Код активации",
        message=f"Ваш код активации: {user.ver_code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )

