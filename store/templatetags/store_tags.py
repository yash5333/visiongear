from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def star_rating(value):
    """Generate star rating HTML"""
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0
    full = int(value)
    half = 1 if (value - full) >= 0.5 else 0
    empty = 5 - full - half
    html = ''
    html += '<i class="fas fa-star text-warning"></i>' * full
    if half:
        html += '<i class="fas fa-star-half-alt text-warning"></i>'
    html += '<i class="far fa-star text-warning"></i>' * empty
    return mark_safe(html)


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def range_tag(n):
    return range(1, n + 1)


@register.inclusion_tag('store/product_image.html')
def product_image(product, css_class=''):
    """Render product image or beautiful placeholder"""
    icons = {
        'cameras': 'fa-camera',
        'tripods': 'fa-podcast',
        'lighting': 'fa-lightbulb',
        'bags': 'fa-briefcase',
    }
    icon = icons.get(product.category.slug, 'fa-camera')
    return {
        'product': product,
        'icon': icon,
        'css_class': css_class,
        'has_image': bool(product.image),
    }
