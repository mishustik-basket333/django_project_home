from django.shortcuts import render

from catalog.models import Product


def home(request):
    context = {
        'title': "Домашняя страница из задания 19.1",
    }
    return render(request, 'catalog/home.html', context)



def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name}: {phone} или {message}")

    return render(request, 'catalog/contacts.html')

def product(request):
    context = {
        'object_list': Product.objects.all(),
        'title': "Продукты ",
    }
    return render(request, 'catalog/product.html', context)

def one_product(request):
    context = {
        'object_list': Product.objects.all(),
        'title': "Продукт - описание",
    }
    return render(request, 'catalog/one_product.html', context)

# def one_product(request, pk):
#     context = {
#         'object_list': Product.objects.get(id=pk),
#         'title': "Продукт - описание",
#     }
#     return render(request, 'catalog/one_product.html', context)
