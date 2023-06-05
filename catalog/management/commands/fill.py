import json

from django.core.management import BaseCommand

from catalog.models import Category, Product, BlogEntry


class Command(BaseCommand):
    def handle(self, *args, **options):

        category_data = []
        product_data = []
        blog_data = []

        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)

        Category.objects.all().delete()
        for raw in data:
            if raw["model"] == "catalog.category":
                category_data.append(Category(**raw["fields"]))
        Category.objects.bulk_create(category_data)

        Product.objects.all().delete()
        for raw in data:
            if raw["model"] == "catalog.product":
                num = raw["fields"]["category"]

                for cat in data:
                    if cat["model"] == "catalog.category" and num == cat["pk"]:
                        a = Category.objects.get(name=cat["fields"]["name"]).id

                raw["fields"]["category"] = Category.objects.get(pk=a)
                product_data.append(Product(**raw["fields"]))
        Product.objects.bulk_create(product_data)

        BlogEntry.objects.all().delete()
        for raw in data:
            if raw["model"] == "catalog.blogentry":
                blog_data.append(BlogEntry(**raw["fields"]))
        BlogEntry.objects.bulk_create(blog_data)



        print("Были удалены все данные из таблиц: Category, Product, BlogEntry\n"
              "Добавлены новые данные из файла 'data.json' в эти таблицы")
