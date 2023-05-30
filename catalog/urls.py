from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product,  one_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', product, name='product'),
    path('contacts/', contacts, name='contacts'),
    path('home/', home, name='home'),
    # path('one_product/', one_product, name='one_product'),
    path('one_product/<int:pk>/', one_product, name='one_product'),
]
