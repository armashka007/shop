from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product


def home(request):
    """Home page view"""
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_active=True)[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'catalog/home.html', context)


def category_list(request):
    """Category list view"""
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'catalog/category_list.html', context)


def product_list(request, slug=None):
    """Product list with filters, search, and pagination"""
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    
    # Filter by category
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    
    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by availability
    in_stock_only = request.GET.get('in_stock', '')
    if in_stock_only:
        products = products.filter(stock__gt=0)
    
    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page', 1)
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'category': category if slug else None,
        'search_query': search_query,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_only': in_stock_only,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
