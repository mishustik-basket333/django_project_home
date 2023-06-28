from django.db import models
from django.utils.text import slugify
from transliterate import translit

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """Класс, для отображения категорий"""
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'категории'  # Настройка для наименования набора объектов
        ordering = ('name',)  # Сортировка по имени


class Product(models.Model):
    """Класс, для отображения продуктов"""
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    picture = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    price = models.FloatField(verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='изменен', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.name} {self.price}'

    class Meta:
        verbose_name = 'продукт'  # Настройка для наименования одного объекта
        verbose_name_plural = 'продукты'  # Настройка для наименования набора объектов
        ordering = ('name',)  # Сортировка по имени


class BlogEntry(models.Model):
    heading = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name='URL', unique=True, db_index=True)
    description = models.TextField(verbose_name='содержимое', **NULLABLE)
    picture = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан', **NULLABLE)
    publication_flag = models.BooleanField(default=True, verbose_name='публикация')
    count_views = models.IntegerField(default=0, verbose_name='кол-во просмотров')

    def counter(self):
        self.count_views += 1
        self.save()

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # Newly created object, so set slug
    #         self.slugs = slugify(self.heading)
    #
    #     super(BlogEntry, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.heading)
        self.slug = translit(self.heading, language_code='ru', reversed=True).lower()
        super().save()

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.heading}'

    def delete(self, *args, **kwargs):
        self.publication_flag = False
        self.save()

    class Meta:
        verbose_name = 'публикация'  # Настройка для наименования одного объекта
        verbose_name_plural = 'публикации'  # Настройка для наименования набора объектов
        ordering = ('heading',)  # Сортировка по заголовку


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='продукт')
    name = models.CharField(max_length=100, verbose_name='название')
    num_version = models.IntegerField(verbose_name='версия')
    flag_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"

    def __str__(self):
        return self.name
