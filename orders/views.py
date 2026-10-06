from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from catalog.models import Product
from .models import Order, OrderItem


def checkout(request):
    """Checkout page"""
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart:view')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        
        if not all([full_name, phone, address]):
            return render(request, 'orders/checkout.html', {'error': 'Заполните все поля'})
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
        )
        
        # Create order items
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                if product.stock < quantity:
                    # Not enough stock, cancel order
                    order.delete()  # Delete the order if any item fails
                    return render(request, 'orders/checkout.html', {
                        'error': f'Недостаточно товара "{product.name}" на складе. Доступно: {product.stock} шт.',
                        'cart_items': cart_items,
                        'total_price': total_price,
                    })
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )
                # Decrease stock
                product.stock -= quantity
                product.save()
            except Product.DoesNotExist:
                pass
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        return redirect('orders:success', order_id=order.id)
    
    # Prepare cart items
    cart_items = []
    total_price = 0
    
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
        except Product.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/checkout.html', context)


def order_success(request, order_id):
    """Order success page"""
    try:
        order = Order.objects.get(id=order_id)
        # Check if user has permission to view this order
        if order.user and order.user != request.user:
            return redirect('catalog:home')
    except Order.DoesNotExist:
        return redirect('catalog:home')
    
    context = {'order': order}
    return render(request, 'orders/order_success.html', context)


@login_required(login_url='accounts:login')
def my_orders(request):
    """User's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'current_status': status,
    }
    return render(request, 'orders/my_orders.html', context)


@login_required(login_url='accounts:login')
def order_detail(request, order_id):
    """Order detail page"""
    try:
        order = Order.objects.get(id=order_id)
        # Check if user has permission to view this order
        if order.user != request.user:
            return redirect('orders:my_orders')
    except Order.DoesNotExist:
        return redirect('orders:my_orders')
    
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)


def order_track(request, order_id):
    """Track order by ID (no auth required)"""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'orders/order_track.html', {'error': 'Заказ не найден'})
    
    context = {'order': order}
    return render(request, 'orders/order_track.html', context)


def order_search(request):
    """Search order by ID"""
    if request.method == 'GET' and 'order_id' in request.GET:
        order_id = request.GET.get('order_id')
        try:
            order_id = int(order_id)
            return redirect('orders:track', order_id=order_id)
        except (ValueError, TypeError):
            pass
    
    return render(request, 'orders/order_search.html', {'error': 'Введите корректный номер заказа'})
