# написано для магазину продуктів

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Product, Order, OrderItem


def product_list(request):
    categories = Category.objects.prefetch_related('products').all()
    products = Product.objects.filter(is_available=True).select_related('category')

    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    featured = Product.objects.filter(is_featured=True, is_available=True)[:6]

    return render(request, 'store/product_list.html', {
        'categories': categories,
        'products': products,
        'featured': featured,
        'selected_category': selected_category,
    })


def cart_view(request):
    cart = _get_cart(request)
    product_ids = [int(k) for k in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for product in products:
        qty = cart.get(str(product.id), 0)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    cart = _get_cart(request)
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    request.session['cart'] = cart
    return JsonResponse({'success': True, 'count': sum(cart.values())})


@require_POST
def cart_remove(request, product_id):
    cart = _get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def cart_update(request, product_id):
    cart = _get_cart(request)
    pid = str(product_id)
    qty = int(request.POST.get('qty', 1))
    if qty > 0:
        cart[pid] = qty
    else:
        cart.pop(pid, None)
    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('product_list')

    product_ids = [int(k) for k in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for product in products:
        qty = cart.get(str(product.id), 0)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'qty': qty, 'subtotal': subtotal})

    if request.method == 'POST':
        order = Order.objects.create(
            full_name=request.POST.get('full_name', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', ''),
            notes=request.POST.get('notes', ''),
            total_price=total,
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['product'].price,
            )
        request.session['cart'] = {}
        return redirect('order_success', pk=order.pk)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/order_success.html', {'order': order})


def _get_cart(request):
    return request.session.get('cart', {})
