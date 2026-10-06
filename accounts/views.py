from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from orders.models import Order


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'catalog:home')
            return redirect(next_url)
        else:
            return render(request, 'accounts/login.html', {'error': 'Неверное имя пользователя или пароль'})
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('catalog:home')


@login_required(login_url='accounts:login')
def profile(request):
    """User profile"""
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': user_orders}
    return render(request, 'accounts/profile.html', context)
