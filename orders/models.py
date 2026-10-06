from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class Order(models.Model):
    """Order model"""
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('processing', 'Обработка'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ('id',)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total_price(self):
        return self.price * self.quantity
