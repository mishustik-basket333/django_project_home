from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, BlogEntry, Version
from catalog.services import get_versions_cache, get_categories_cache


class HomeListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/home.html"
    extra_context = {
        'title': "Домашняя страница из задания 19.1",
        "head": "19.1"
    }
    login_url = '/login/'


# def home(request):
#     context = {
#         'title': "Домашняя страница из задания 19.1",
#     }
#     return render(request, 'catalog/home.html', context)


@login_required(login_url='/login/')
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name}: {phone} или {message}")

    return render(request, 'catalog/contacts.html')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product.html"
    extra_context = {
        'title': "Продукты",
        "head": "Все продукты"
    }
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["version"] = get_versions_cache()
        context_data['categories']: get_categories_cache()
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication_flag=True)
        # if not self.queryset.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)
        return queryset


# def product(request):
#     context = {
#         'object_list': Product.objects.all(),
#         'title': "Продукты",
#     }
#     return render(request, 'catalog/product.html', context)


class OneProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/one_product_update.html"
    success_url = reverse_lazy("catalog:product")
    permission_required = 'catalog.change_product'

    def test_func(self):
        return self.request.user == self.get_object().owner

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Описание про: " + self.get_object().name.lower()
        context_data["head"] = self.get_object().name

        # Формирование формсета
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class OneProductDetailView(DetailView):
    model = Product
    template_name = "catalog/one_product.html"

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Описание про: " + self.get_object().name.lower()
        context_data["head"] = self.get_object().name

        # Формирование формсета
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    # def one_product(request, pk):
    #     context = {
    #         'object': Product.objects.get(pk=pk),
    #         'title': "Продукт - описание",
    #     }
    #     return render(request, 'catalog/one_product.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product")

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

        return super().form_valid(form)


class OneProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product")
    permission_required = 'catalog.delete_product'


class BlogEntryCreateView(CreateView):
    model = BlogEntry
    fields = ("heading", "description", "picture", 'publication_flag',)
    template_name = "catalog/blog_entry_form.html"
    success_url = reverse_lazy("catalog:blog_entry")


class BlogEntryListView(ListView):
    model = BlogEntry
    extra_context = {
        'title': "Блоги",
        "head": "Все блоги"
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication_flag=True, )
        return queryset


class OneBlogEntryDetailView(DetailView):
    form_class = BlogEntry
    template_name = "catalog/one_blog_entry_detail.html"

    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data["title"] = "Статья про: " + self.get_object().heading.lower()
        contex_data["head"] = self.get_object().heading
        return contex_data

    def get_queryset(self):
        return BlogEntry.objects.filter(slug=self.kwargs['slug'])


class BlogEntryUpdateView(UpdateView):
    model = BlogEntry
    fields = ("heading", "description", "picture", 'publication_flag',)
    template_name = "catalog/blog_entry_form.html"

    # success_url = reverse_lazy("catalog:one_blog_entry")

    def get_success_url(self):
        return reverse_lazy('catalog:one_blog_entry', kwargs={'slug': self.kwargs['slug']})


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    # template_name = "catalog/blog_entry_form.html"
    success_url = reverse_lazy("catalog:blog_entry")
