from django.contrib import admin
from .models import OrderItem, Order

"""
Мы используем ModelInline для модели OrderItem в OrderAdmin, чтобы включить ее в класс OrderAdmin.
Inline помогает нам поместить модель на страницу редактирования родительской модели.
""" 
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
 
 
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
 
 
admin.site.register(Order, OrderAdmin)


