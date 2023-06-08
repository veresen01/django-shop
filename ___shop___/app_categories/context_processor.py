from django.db import OperationalError

from app_product.models import Category
from app_product.models import Product


def category_context(request):
    context = dict()
    try:
        categories: Category = Category.objects.filter(
            parent=None,
            active=True
        ).order_by('sort_index')
    except OperationalError:
        pass
    else:
        context['categories'] = categories
    
    return context
