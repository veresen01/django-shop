from random import randint

from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your views here.
from django.views import generic

from app_cart.cart import Cart
from app_cart.utils import is_ajax
from app_orders.models import DeliveryMethod
from app_orders.models import Order
from app_orders.models import OrderItems
from app_orders.models import PaymentMethod
from app_orders.models import PaymentStatuses
from app_product.models import Product
from app_settings.models import SiteSettings
from app_users.forms import RegForm


class OrderView(generic.TemplateView):
    template_name = 'pages/orders/order.html'
    page_title = _('Оформление заказа')
    page_description = _('Оформление заказа')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            instance = self.request.user
            context['form_reg'] = RegForm(instance=instance)
            context['form_reg'].fields['email'].disabled = True
            context['form_reg'].fields['full_name'].disabled = True
            context['form_reg'].fields['phoneNumber'].disabled = True
        else:
            context['form_reg'] = RegForm()
        # return context
        
        settings: SiteSettings = SiteSettings.load()
        
        # deliveries: DeliveryMethod = DeliveryMethod.objects.all()
        # delivery: DeliveryMethod
        # for delivery in deliveries:
        #     delivery.description = _(delivery.description)
        #     delivery.description = delivery.description.format(
        #         DELIVERY_LIMIT=settings.order_delivery_limit,
        #         DELIVERY_PRICE=settings.order_delivery_price,
        #         DELIVERY_EXPRESS_PRICE=settings.order_delivery_express
        #     )
        
        cart = Cart(self.request)
        
        context['cart'] = cart
        # context['deliveries'] = deliveries
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        context['section_column'] = " Section_column Section_columnRight Section_columnWide Order"
        return context


class OrderDetail(generic.DetailView):
    template_name = 'pages/orders/order_detail.html'
    model = Order
    page_title = _('Заказ №{}')
    page_subtitle = _('История заказов')
    page_description = _('Детали заказа №{}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order: Order = self.object
        # print(f'{order=}')
        # print(f'{order.get_items()=}')
        # print(f'{order.get_total_items()=}')
        # print(f'{order.get_total_price()=}')
        # print(f'{order.get_price_with_delivery()=}')
        context['page_title'] = self.page_title.format(order.id)
        context['page_subtitle'] = self.page_subtitle.format(order.id)
        context['page_prev_breadcrumbs'] = reverse('users:history_orders')
        context['page_description'] = self.page_description.format(order.id)
    
        return context


class OrderDetailPayment(generic.DetailView):
    template_name = 'pages/orders/order_detail_payment.html'
    model = Order
    context_object_name = 'order'
    page_title = _('Оплата')
    page_description = _('Оплата заказа')
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetailPayment, self).get_context_data(**kwargs)
        
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        
        return context


class OrderPaymentProcess(generic.TemplateView):
    template_name = 'pages/orders/order_payment_process.html'
    page_title = _('Ожидание оплаты')
    page_description = _('Ожидание оплаты')
    
    def post(self, request: HttpRequest, *args, **kwargs):
        # sleep(randint(3, 8))
        context = super().get_context_data(**kwargs)
        
        # self.object = self.get_object()
        
        print(f'{request.POST=}')
        
        order_id = request.POST.get('order', 0)
        card_number: str = request.POST.get('id_card_number', 0)
        order: Order = Order.objects.filter(
            pk=order_id
        )
        if order.exists():
            order = order.first()
            context['order'] = order
            if not card_number.endswith('0'):
                # подтвердить оплату заказа
                new_status: PaymentStatuses = PaymentStatuses.objects.get(pk=3)
                order.payment_status = new_status
                order.payment_at = timezone.now()
                order.save()
            else:
                # выдать рандомную ошибку
                payment_error = randint(4, 6)
                new_status: PaymentStatuses = PaymentStatuses.objects.get(pk=payment_error)
                order.payment_status = new_status
                order.save()
        else:
            context['error'] = _('Такого заказа не существует')
        
        # context['error'] = 'test'
        
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        
        return self.render_to_response(context=context)


def create_order(request: HttpRequest):
    """
    AJAX-REQUEST - Создание заказа
    :param request:
    :return:
    """
    response = dict()
    response['action'] = 'create_order'
    response['msg'] = f"init {response['action']}"
    response['result'] = False
    
    response['post'] = request.POST
    
    prepared_items = []
    
    if request.method == "POST" and is_ajax(request):
        cart = Cart(request)
        item: dict
        for item in cart.__iter__():
            # print(f'{item=}')
            product: Product = item.get('product')
            amount = item.get('quantity')
            if product.remains >= amount:
                prepared_items.append(item)
            else:
                response['msg'] = _('ОШИБКА: Товара "<b>{}</b>" не осталось на складе. Проверьте корзину!').format(
                    product.title)
                break
        
        if len(prepared_items) > 0:
            go_next = False
            payment = request.POST.get('pay_value', 0)
            # проверяем наличие способа оплаты
            payment_method: PaymentMethod = PaymentMethod.objects.filter(
                pk=payment
            )
            
            if payment_method.exists():
                payment_method = payment_method.first()
                go_next = True
            else:
                response['msg'] = _('Такого способа оплаты не существует')
            
            if go_next:
                go_next = False
                # проверяем способ доставки
                delivery = request.POST.get('delivery_value', 0)
                
                delivery_method: DeliveryMethod = DeliveryMethod.objects.filter(
                    pk=delivery
                )
                
                if delivery_method.exists():
                    delivery_method = delivery_method.first()
                    go_next = True
                else:
                    response['msg'] = _('Такого способа доставки не существует')
            
            if go_next:
                go_next = False
                # создаем Order
                payment_status: PaymentStatuses = PaymentStatuses.objects.get(pk=1)
                city = request.POST.get('city', '')
                address = request.POST.get('address', '')
                order: Order = Order.objects.create(
                    user=request.user,
                    method_payment=payment_method,
                    method_delivery=delivery_method,
                    payment_status=payment_status,
                    city=city,
                    address=address
                )
                
                if order.id:
                    go_next = True
                else:
                    response['msg'] = _('Ошибка при создании заказа')
            
            if go_next:
                item: dict
                for item in prepared_items:
                    product: Product = item.get('product')
                    amount = item.get('quantity')
                    price = item.get('price')
                    order_item: OrderItems = OrderItems.objects.create(
                        order=order,
                        product=product,
                        product_amount=amount,
                        product_price=price
                    )
                    if not order_item.id:
                        go_next = False
                        OrderItems.objects.filter(
                            order=order
                        ).delete()
                        Order.objects.filter(
                            pk=order.id
                        ).delete()
                        response['msg'] = _('Ошибка при добавлении товара в заказ!')
                        break
                    else:
                        go_next = True
                        # бронирование товара
                        # при отмене заказа, количество возвращается из amount в remains
                        product.remains -= amount
                        product.save()
            
            if go_next:
                cart.clear()
                response['order'] = order.id
                response['result'] = True
    else:
        response['msg'] = _('Неверно создан запрос')
    
    return JsonResponse(response)


class OrderCancelView(generic.TemplateView):
    template_name = 'pages/orders/order_canceled.html'
    page_title = _('Отмена заказа')
    page_description = _('Заказ был отменен')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
    
        return context
    

def cancel_order(request: HttpRequest):
    """
    AJAX-REQUEST - Отмена заказа
    :param request:
    :return:
    """
    response = dict()
    response['action'] = 'cancel_order'
    response['msg'] = f"init {response['action']}"
    response['result'] = False
    
    response['post'] = request.POST
    
    if request.method == "POST" and is_ajax(request):
        order_id = request.POST.get('order_id', 0)
        print(f'{order_id=}')
        order: Order = Order.objects.filter(
            pk=order_id,
            user=request.user
        )
        if order.exists():
            order: Order = order.first()
            order_item: OrderItems
            for order_item in order.order.all():
                print(f'{order_item=}')
                product: Product = Product.objects.get(pk=order_item.product.id)
                product.remains += order_item.product_amount
                product.save()
                order_item.delete()

            order.delete()

            response['result'] = True

        else:
            response['msg'] = _('Такого заказа не существует')
    else:
        response['msg'] = _('Неверно создан запрос')
    
    return JsonResponse(response)
