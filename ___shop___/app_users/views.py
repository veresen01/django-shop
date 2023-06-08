# Create your views here.
from contextlib import suppress

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic import CreateView
from loguru import logger

from app_orders.models import Order
from app_product.models import HistoryProduct
from app_settings.models import SiteSettings
from app_users.forms import RegForm
# from app_users.models import Profile
from app_users.forms import UpdateProfileForm
from app_users.forms import User


class MyLoginView(views.LoginView):
    template_name = 'pages/account/login.html'
    page_title = _('Авторизация')
    page_description = _('Авторизация')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        return context


class SignUpView(CreateView):
    model = User
    form_class = RegForm
    template_name = 'pages/account/signup.html'
    success_url = reverse_lazy('shop:index')
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('users:account'))
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = RegForm(request.POST, request.FILES)
        self.object = None
        
        # phone = request.POST.get('phoneNumber', '')
        # logger.debug(f'Before clean: {phone=}')
        # phone = clear_phone(phone)
        # logger.debug(f'After clean: {phone=}')
        # form.phoneNumber = phone
        #
        # phone = form.cleaned_data.get('phoneNumber')
        # logger.debug(f'In form before valid: {phone=}')
        
        if form.is_valid():
            form.save()
            # phone = form.cleaned_data.get('phoneNumber')
            # logger.debug(f'In form after valid: {phone=}')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            with suppress(ObjectDoesNotExist):
                my_group = Group.objects.get(name='Пользователи')
                my_group.user_set.add(user)
            login(request, user)
            return HttpResponseRedirect(self.success_url)
        return self.form_invalid(form)


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'pages/account/account.html'
    page_title = _('Личный кабинет')
    page_description = _('Личный кабинет')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        order: Order = Order.objects.order_by('-create_at')[:1]
        
        if order.exists():
            order = order.first()
            context['last_order'] = order
        
        context['page_title'] = self.page_title
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        context['section_column'] = " Section_column Section_columnLeft"
        return context


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'pages/account/profile.html'
    page_title = _('Профиль')
    page_description = _('Профиль')
    
    # form_class = UpdateProfileForm
    # model = User
    # raise_exception = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user: User = User.objects.get(pk=self.request.user.id)
        
        form = UpdateProfileForm(
            initial={
                'phoneNumber': user.phoneNumber,
                'full_name': f'{user.full_name}',
                'email': user.email,
            }
        )
        
        context['page_title'] = self.page_title
        context['form'] = form
        context['page_description'] = self.page_description
        context['section_column'] = " Section_column Section_columnLeft"
        return context
    
    # def get_success_url(self):
    #     return reverse('users:profile')
    
    # def get_object(self, queryset=None):
    #     return self.request.user
    #
    # def form_valid(self, form):
    #     messages.info(self.request, "Профиль успешно сохранен")
    #     return super(ProfileView, self).form_valid(form)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        
        form = UpdateProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phoneNumber')
            full_name = form.cleaned_data.get('full_name')
            
            go_next = False
            if len(password1):
                if password1 != password2:
                    form.add_error('password2', _('Пароли должны совпадать'))
                else:
                    request.user.set_password(password1)
                    request.user.save()
                    user = authenticate(username=request.user.email, password=password1)
                    login(request, user)
                    go_next = True
            else:
                go_next = True
            
            if go_next:
                go_next = False
                exists_email: User = User.objects.filter(
                    email=email
                ).exclude(
                    id=request.user.id
                )
                logger.info(f'{exists_email=}')
                if exists_email.exists():
                    form.add_error('email', _('Такая почта уже зарегистрирована!'))
                else:
                    go_next = True
            
            if go_next:
                go_next = False
                exists_phone: User = User.objects.filter(
                    phoneNumber=phone
                ).exclude(
                    id=request.user.id
                )
                logger.info(f'{exists_phone=}')
                if exists_phone.exists():
                    form.add_error('phone', _('Такой телефон уже зарегистрирован!'))
                else:
                    go_next = True
            
            if go_next:
                request.user.email = email
                request.user.phoneNumber = phone
                request.user.full_name = full_name
                
                messages.info(self.request, "Профиль успешно сохранен")
        
        context['form'] = form
        context['section_column'] = " Section_column Section_columnLeft"
        
        return self.render_to_response(context=context)


class HistoryOrdersListView(generic.ListView):
    template_name = 'pages/account/history_orders.html'
    page_title = _('История заказов')
    page_description = _('История заказов')
    context_object_name = 'orders'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        context['section_column'] = " Section_column Section_columnLeft"
        return context


class HistoryProductsListView(generic.ListView):
    template_name = 'pages/account/history_products.html'
    page_title = _('История просмотров')
    page_description = _('История просмотров')
    model = HistoryProduct
    context_object_name = 'products_list'
    
    def get(self, request: HttpRequest, *args, **kwargs):
        settings: SiteSettings = SiteSettings.load()
        self.paginate_by = 2
        if settings.product_page_amount:
            self.paginate_by = settings.product_page_amount
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        context['section_column'] = " Section_column Section_columnLeft"
        return context


class LogOutView(views.LogoutView):
    template_name = 'general/auth/logout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        logout_page_data = self.request.META['HTTP_REFERER']
        host_data: str = self.request.META['HTTP_HOST']
        
        logout_page_arr: list = logout_page_data.split(host_data + '/')
        
        if len(logout_page_arr) >= 2:
            logout_page = logout_page_arr[1]
        else:
            logout_page = '/'
        
        context['logout_page'] = logout_page
        
        return context


class RecoveryView(generic.TemplateView):
    template_name = 'pages/account/recovery.html'
    page_title = _('Восстановление доступа')
    page_description = _('Восстановление доступа')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        return context
