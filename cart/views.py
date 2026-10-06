from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from catalog.models import Product


def cart_view(request):
    """Display shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_quantity = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
            total_price += item_total
            total_quantity += quantity
        except Product.DoesNotExist:
            # Remove deleted products from cart
            del cart[product_id]
    
    request.session['cart'] = cart
    request.session.modified = True
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    # Validate quantity
    if quantity > product.stock:
        quantity = product.stock
    
    if quantity < 1:
        quantity = 1
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += quantity
        # Ensure total doesn't exceed stock
        if cart[product_id_str] > product.stock:
            cart[product_id_str] = product.stock
    else:
        cart[product_id_str] = quantity
    
    request.session['cart'] = cart
    request.session.modified = True
    
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} добавлен в корзину',
            'cart_count': sum(cart.values())
        })
    
    return redirect('cart:view')


@require_POST
def remove_from_cart(request, product_id):
    """Remove product from cart"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('cart:view')


@require_POST
def update_cart(request, product_id):
    """Update product quantity in cart"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if product_id_str in cart:
        product = get_object_or_404(Product, id=product_id)
        
        # Validate quantity
        if quantity > product.stock:
            quantity = product.stock
        
        if quantity < 1:
            del cart[product_id_str]
        else:
            cart[product_id_str] = quantity
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('cart:view')


@require_POST
def clear_cart(request):
    """Clear entire cart"""
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart:view')


def get_cart_info(request):
    """Get cart info as JSON"""
    cart = request.session.get('cart', {})
    total_quantity = sum(cart.values())
    total_price = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            total_price += float(product.price) * quantity
        except Product.DoesNotExist:
            pass
    
    return JsonResponse({
        'quantity': total_quantity,
        'total': float(total_price),
        'count': len(cart),
    })
