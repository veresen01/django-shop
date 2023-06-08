from django.db import connection

from app_product.models import Category
from app_product.models import Product


def get_range_price(category: Category = None):
    min_price = 0
    max_price = 0
    print(f'get_range_price > {category=}')
    if db_table_exists('products'):
        if category is None:
            product: Product = Product.objects.filter(
                active=True
            )
        else:
            product: Product = Product.objects.filter(
                category=category,
                active=True
            )
        
        product_min_price = product.order_by('price').values('price')
        product_max_price = product.order_by('-price').values('price')
        
        if product_min_price.exists():
            product_min_price: dict = product_min_price.first()
            min_price = product_min_price.get('price', 0)
        
        if product_max_price.exists():
            product_max_price: dict = product_max_price.first()
            max_price = product_max_price.get('price', 0)
        
    return {
        'min_price': min_price,
        'max_price': max_price
    }


def isint(s):
    if s:
        try:
            int(s)
            return True
        except ValueError:
            return False
    return False


def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()
