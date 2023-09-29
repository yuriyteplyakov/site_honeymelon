from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'catalog/product/list.html',
                  {'category': category, 'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'catalog/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

def product_list_order(request, category_slug=None):
    category = None
    categories = Category.objects.filter(products__available=False).distinct()
    products = Product.objects.filter(available=False)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'catalog/product/list_order.html',
                  {'category': category, 'categories': categories,
                   'products': products})

def product_detail_order(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=False)
    cart_product_form = CartAddProductForm()
    return render(request, 'catalog/product/detail_order.html', {'product': product, 'cart_product_form': cart_product_form})