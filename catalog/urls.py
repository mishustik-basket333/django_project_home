from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, OneProductDetailView, HomeListView, BlogEntryListView, \
    OneBlogEntryDetailView, BlogEntryCreateView, BlogEntryUpdateView, BlogEntryDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product'),
    path('contacts/', contacts, name='contacts'),
    path('home/', HomeListView.as_view(), name='home'),
    path('one_product/<int:pk>/', OneProductDetailView.as_view(), name='one_product'),
    path('blog_entry/', BlogEntryListView.as_view(), name='blog_entry'),
    path('one_blog_entry_detail/<slug>/', OneBlogEntryDetailView.as_view(), name='one_blog_entry'),
    path('blog_entry/create/', BlogEntryCreateView.as_view(), name='blog_entry_create'),
    path('blog_entry/update/<slug>', BlogEntryUpdateView.as_view(), name='blog_entry_update'),
    path('blog_entry/delete/<slug>', BlogEntryDeleteView.as_view(), name='blog_entry_delete'),

]
