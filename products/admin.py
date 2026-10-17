
from django.contrib import admin
from .models import Product, Order, OrderItem

admin.site.register(Product)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone')
    list_editable = ('status',)
    ordering = ('-created_at',)


admin.site.register(OrderItem)

