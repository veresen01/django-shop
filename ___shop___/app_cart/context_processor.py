from app_cart.cart import Cart


def cart_processor(request):
    cart: Cart = Cart(request)
    
    return {
        'total_price': cart.get_total_price(),
        'total_items': cart.__len__()
    }
