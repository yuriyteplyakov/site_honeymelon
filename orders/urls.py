from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create_order/', views.order_create, name='order_create'), 
    ]