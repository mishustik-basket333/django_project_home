import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        category_data = []
        product_data = []
        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)

        for raw in data:
            if raw["model"] == "catalog.category":
                category_data.append(Category(**raw["fields"]))
            elif raw["model"] == "catalog.product":
                num = raw["fields"]["category"]
                raw["fields"]["category"] = Category(**data[num]["fields"])
                product_data.append(Product(**raw["fields"]))
        Category.objects.bulk_create(category_data)
        # Product.objects.bulk_create(product_data)
        print(product_data)
        print("Были удалены все данные из таблиц: Category, Product\n"
              "Добавлены новые данные из файла 'data.json' в эти таблицы")


