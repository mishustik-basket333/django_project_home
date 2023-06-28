from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, OneProductDetailView, HomeListView, BlogEntryListView, \
    OneBlogEntryDetailView, BlogEntryCreateView, BlogEntryUpdateView, BlogEntryDeleteView, ProductCreateView, \
    OneProductUpdateView, OneProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('home/', HomeListView.as_view(), name='home'),

    path('', ProductListView.as_view(), name='product'),
    path('product/<int:pk>/', OneProductDetailView.as_view(), name='one_product'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>', OneProductUpdateView.as_view(), name='one_product_update'),
    path('product/delete/<int:pk>', OneProductDeleteView.as_view(), name='one_product_delete'),

    path('blog_entry/', BlogEntryListView.as_view(), name='blog_entry'),
    path('one_blog_entry_detail/<slug>/', OneBlogEntryDetailView.as_view(), name='one_blog_entry'),
    path('blog_entry/create/', BlogEntryCreateView.as_view(), name='blog_entry_create'),
    path('blog_entry/update/<slug>', BlogEntryUpdateView.as_view(), name='blog_entry_update'),
    path('blog_entry/delete/<slug>', BlogEntryDeleteView.as_view(), name='blog_entry_delete'),

]
