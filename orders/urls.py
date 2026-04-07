from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place/', views.place_order, name='place_order'),
    path('success/<uuid:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('detail/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('cancel/<uuid:order_id>/', views.cancel_order, name='cancel_order'),
    path('invoice/<uuid:order_id>/', views.invoice, name='invoice'),
    # Admin
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/products/', views.admin_products, name='admin_products'),
]
