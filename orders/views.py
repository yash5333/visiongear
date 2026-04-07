from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from store.models import Cart, CartItem
from .models import Order, OrderItem
from decimal import Decimal
import uuid
import json


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')

    profile = request.user.profile
    initial_data = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
        'phone': profile.phone,
        'address': profile.address,
        'city': profile.city,
        'state': profile.state,
        'pincode': profile.pincode,
        'country': profile.country or 'India',
    }

    subtotal = cart.total
    shipping = Decimal('0') if subtotal > Decimal('5000') else Decimal('199')
    tax = round(subtotal * Decimal('0.18'), 2)
    total = subtotal + shipping + tax

    context = {
        'cart': cart,
        'initial_data': initial_data,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def place_order(request):
    if request.method != 'POST':
        return redirect('orders:checkout')

    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')

    subtotal = cart.total
    shipping = Decimal('0') if subtotal > Decimal('5000') else Decimal('199')
    tax = round(subtotal * Decimal('0.18'), 2)
    total = subtotal + shipping + tax

    order = Order.objects.create(
        user=request.user,
        full_name=request.POST.get('full_name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        state=request.POST.get('state'),
        pincode=request.POST.get('pincode'),
        country=request.POST.get('country', 'India'),
        notes=request.POST.get('notes', ''),
        subtotal=subtotal,
        shipping_cost=shipping,
        tax=tax,
        total=total,
        payment_method=request.POST.get('payment_method', 'demo'),
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_price=item.product.effective_price,
            quantity=item.quantity,
        )
        # Reduce stock
        item.product.stock = max(0, item.product.stock - item.quantity)
        item.product.save()

    # Clear cart
    cart.items.all().delete()

    # Simulate payment processing
    order.payment_status = 'paid'
    order.status = 'confirmed'
    order.transaction_id = f'TXN{str(uuid.uuid4()).replace("-","").upper()[:12]}'
    order.save()

    messages.success(request, f'Order #{order.short_id} placed successfully!')
    return redirect('orders:order_success', order_id=order.order_id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.short_id} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('orders:order_detail', order_id=order_id)


@login_required
def invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})


# ── Admin dashboard views ──────────────────────────────────────────────
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User as AuthUser
from django.db.models import Sum, Count
from django.utils import timezone
import datetime


@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(Sum('total'))['total__sum'] or 0
    total_users = AuthUser.objects.count()
    from store.models import Product
    total_products = Product.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:10]
    pending_orders = Order.objects.filter(status='pending').count()

    # Sales by month (last 6 months)
    months = []
    revenue_data = []
    for i in range(5, -1, -1):
        d = timezone.now() - datetime.timedelta(days=30 * i)
        label = d.strftime('%b %Y')
        rev = Order.objects.filter(
            created_at__year=d.year,
            created_at__month=d.month,
            payment_status='paid'
        ).aggregate(Sum('total'))['total__sum'] or 0
        months.append(label)
        revenue_data.append(float(rev))

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'pending_orders': pending_orders,
        'months': json.dumps(months),
        'revenue_data': json.dumps(revenue_data),
    }
    return render(request, 'orders/admin_dashboard.html', context)


@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'orders/admin_orders.html', {'orders': orders, 'status_filter': status_filter})


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.short_id} status updated to {new_status}.')
    return redirect('orders:admin_orders')


@staff_member_required
def admin_users(request):
    users = AuthUser.objects.all().order_by('-date_joined')
    return render(request, 'orders/admin_users.html', {'users': users})


@staff_member_required
def admin_products(request):
    from store.models import Product, Category
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'orders/admin_products.html', {'products': products, 'categories': categories})
