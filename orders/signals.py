from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_delete, sender=OrderItem)
def return_stock_on_order_item_delete(sender, instance, **kwargs):
    """Return stock when order item is deleted"""
    product = instance.product
    product.stock += instance.quantity
    product.save()