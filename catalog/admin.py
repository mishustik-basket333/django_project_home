from django.contrib import admin

from catalog.models import Product, Category, BlogEntry, Version


# Register your models here.
# admin.site.register(Product)
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_display_links = ('id', 'name')
    list_filter = ("category", )
    search_fields = ("name", "description")

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return ["name", "picture", "price", "owner"]


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "heading", "slug", "created_at", "count_views", "publication_flag")
    search_fields = ("heading", "description")
    prepopulated_fields = {'slug': ('heading',)}


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "num_version", "flag_active", "product")
    search_fields = ("name", "num_version")
    list_filter = ("name", )
