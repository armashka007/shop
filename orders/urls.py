from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('detail/<int:order_id>/', views.order_detail, name='detail'),
    path('track/<int:order_id>/', views.order_track, name='track'),
    path('search/', views.order_search, name='search'),
]
