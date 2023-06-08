from django.http import HttpRequest
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
# Create your views here.
from django.views import generic

from app_cart.cart import Cart
from app_cart.utils import is_ajax
from app_product.models import Product


class CartView(generic.TemplateView):
    template_name = 'pages/shop/cart.html'
    
    page_title = _('Корзина')
    page_description = _('Корзина')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cart = Cart(self.request)
        
        context['cart'] = cart
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        return context
    
    # def post(self, request: HttpRequest, *args, **kwargs):
    #     # context = super().get_context_data(**kwargs)
    #     return redirect(reverse())


def add_product_in_cart(request: HttpRequest):
    """
    AJAX-REQUEST - Добавление продукта в корзину
    :param request:
    :return:
    """
    response = dict()
    response['action'] = 'add_product_in_cart'
    response['msg'] = f"init {response['action']}"
    response['result'] = False
    
    response['post'] = request.POST
    
    if request.method == "POST" and is_ajax(request):
        product_id = request.POST.get('product_id')
        product_amount = request.POST.get('product_amount', 1)
        product: Product = Product.objects.filter(pk=product_id)
        if product.exists():
            product = product.first()
            
            if product.remains > 0:
                response['result'] = True
                
                cart = Cart(request)
                cart.add(
                    product=product,
                    quantity=int(product_amount),
                    update_quantity=False
                )
                
                product_remains = cart.get_quantity(product_id)
                response['result'] = True
                if product_remains > product.remains:
                    cart.add(
                        product=product,
                        quantity=int(product.remains),
                        update_quantity=True
                    )
                    response['msg'] = _('Количество товара <b>"{}"</b> ограничено! Доступно: {} шт.').format(
                        product.title,
                        product.remains
                    )
                else:
                    response['msg'] = _('Товар <b>"{}"</b> успешно добавлен в корзину').format(product.title)
            
            else:
                response['msg'] = _('Товара нет в наличии')
        
        else:
            response['msg'] = _('Такого товара не существует')
    else:
        response['msg'] = _('Неверно создан запрос')
    
    return JsonResponse(response)


def update_cart_view(request: HttpRequest):
    """
    AJAX-REQUEST - Обновление корзины в шапке
    :param request:
    :return:
    """
    response = dict()
    response['action'] = 'update_cart_view'
    response['msg'] = f"init {response['action']}"
    response['result'] = False
    
    response['post'] = request.POST
    
    if request.method == "POST" and is_ajax(request):
        response['result'] = True
        cart = Cart(request)
        response['total_price'] = cart.get_total_price()
        response['total_items'] = cart.__len__()
    else:
        response['msg'] = _('Неверно создан запрос')
    
    return JsonResponse(response)


def update_product_amount(request: HttpRequest):
    """
    AJAX-REQUEST - Обновление количество товара
    :param request:
    :return:
    """
    response = dict()
    response['action'] = 'update_product_amount'
    response['msg'] = f"init {response['action']}"
    response['result'] = False
    response['debug'] = dict()
    
    response['post'] = request.POST
    
    if request.method == "POST" and is_ajax(request):
        product_id = request.POST.get('product_id')
        product_amount = request.POST.get('product_amount')
        product_update_amount = request.POST.get('product_update_amount', False)
        response['debug']['product_id'] = product_id
        response['debug']['product_amount'] = product_amount
        response['debug']['product_update_amount'] = product_update_amount
        
        product: Product = Product.objects.filter(pk=product_id)
        if product.exists():
            product = product.first()
            
            cart = Cart(request)
            
            if product.remains > 0:
                response['result'] = True
                
                cart.add(
                    product=product,
                    quantity=int(product_amount),
                    update_quantity=product_update_amount
                )
                
                product_remains = cart.get_quantity(product_id)
                response['result'] = True
                if product_remains > product.remains:
                    cart.add(
                        product=product,
                        quantity=int(product.remains),
                        update_quantity=True
                    )
                    response['msg'] = _('Количество товара <b>"{}"</b> ограничено! Доступно: {} шт.').format(
                        product.title,
                        product.remains
                    )
                    response['granted_amount'] = product.remains
                else:
                    response['msg'] = _('Количество товара <b>"{}"</b> успешно обновлено ({})').format(
                        product.title,
                        product_remains
                    )
            
            else:
                response['msg'] = _('Товара нет в наличии')
            
            response['new_total_price'] = cart.get_total_price_product(product_id)
            
            response['result'] = True
        else:
            response['msg'] = _('Такого товара не существует')
    else:
        response['msg'] = _('Неверно создан запрос')
    
    return JsonResponse(response)


def remove_product(request: HttpRequest):
    response = dict()
    response['action'] = 'remove_product'
    response['msg'] = ''
    response['result'] = False
    
    response['post'] = request.POST
    
    if request.method == "POST" and is_ajax(request):
        product_id = request.POST.get('product_id')
        product: Product = Product.objects.filter(pk=product_id)
        if product.exists():
            product = product.first()
            cart = Cart(request)
            cart.remove(product)
            
            response['result'] = True
            response['msg'] = _('Товар <b>"{}"</b> успешно удалён из корзины!').format(product.title)
            
            response['cart_amount'] = cart.__len__()
        
        else:
            response['msg'] = _('Такого товара не существует')
    
    else:
        response['msg'] = _('Неверно создан запрос')
    
    return JsonResponse(response)
