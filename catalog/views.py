from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required

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

@login_required
def all_save_view_products(request):
    user = request.user
    saved_products = user.catalog_products_save.all()
    context = {'saved_products': saved_products}
    return render(request, 'catalog/saved_products.html', context)


"""
было
@login_required
def save_products_is_ajax(request):
    product = get_object_or_404(Product, id=request.POST.get("id"))
    saved = False
    if product.saved_products.filter(id=request.user.id).exists():
        product.saved_products.remove(request.user)
        saved = False
    else:
        product.saved_products.add(request.user)
        saved = True
    context = {
        'product': product,
        'total_saved_products': product.total_saved_products(),
        'saved': saved
    }

    if request.is_ajax():
        html = render_to_string('catalog/save_section.html',
                                context,
                                request=request)
        return JsonResponse({'form':html})
"""

@login_required
def save_products_is_ajax(request):
    product = get_object_or_404(Product, id=request.POST.get("id"))
    saved = False
    if product.saved_products.filter(id=request.user.id).exists():
        product.saved_products.remove(request.user)
        saved = False
    else:
        product.saved_products.add(request.user)
        saved = True
    context = {
        'product': product,
        'total_saved_products': product.total_saved_products(),
        'saved': saved
    }

    html = render_to_string('catalog/save_section.html', context, request=request)
    return JsonResponse({'form': html})