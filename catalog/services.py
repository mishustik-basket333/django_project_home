from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from catalog.models import Version, Category


def send_200views_mail(user):
    send_mail(
        'Просмотры',
        "200 просмотров, ура!!!",
        settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def get_versions_cache():
    if settings.CACHE_ENABLED:
        key = "versions_list"
        version_list = cache.get(key)
        if version_list is None:
            version_list = Version.objects.all()
            cache.set(key, version_list)
    else:
        version_list = Version.objects.all()
    return version_list


def get_categories_cache():
    if settings.CACHE_ENABLED:
        key = 'categories_list'
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = Category.objects.all()
            cache.set(key, categories_list)
    else:
        categories_list = Category.objects.all()
    return categories_list
