from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('catalog-list/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('catalog-list/order/', views.product_list_order, name='product_list_order'),
    path('<slug:category_slug>/order/', views.product_list_order, name='product_list_by_category_order'),
    path('<int:id>/<slug:slug>/', views.product_detail_order, name='product_detail_order'),
]