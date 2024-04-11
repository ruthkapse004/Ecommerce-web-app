from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'email', 'phone', 'membership']
    list_select_related = ['user']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, category):
        # If count=0, don't create url simply pass count.
        count = category.product_count
        if not count:
            return count

        url = (
            reverse("admin:store_product_changelist") + '?' +
            urlencode({
                'category__id': str(category.id)
            })
        )
        return format_html("<a href='{}' >{}</a>", url, category.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category_id',
                    'description', 'price', 'image', ]
    list_editable = ['price', 'image']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_date', 'order_amount',
                    'customer_id', 'customer', 'shipping_address']
    list_select_related = ['customer']

    def get_queryset(self, request):
        query_set = models.Order.objects.filter(complete=True)
        return query_set


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_date',
                    'product_id', 'product', 'quantity']
    list_select_related = ['product']


@admin.register(models.ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'customer',
                    'address', 'city', 'state', 'shipping_date']
    list_select_related = ['customer']
