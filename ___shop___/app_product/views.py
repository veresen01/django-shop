from django.utils.translation import gettext_lazy as _
from django.views import generic

from app_product.models import HistoryProduct
from app_product.models import Product
from app_reviews.forms import ReviewForm


class ProductDetailView(generic.DetailView):
    template_name = 'pages/product/product.html'
    model = Product
    
    page_title = _('Товар')
    page_description = _('О товаре')
    context_object_name = 'product_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        review_add_form = ReviewForm()
        
        product: Product = self.object
        print(f'{product=}')
        
        history_product: HistoryProduct = HistoryProduct.objects.filter(
            user=self.request.user,
            product=product
        )
        if not history_product.exists():
            new_history: HistoryProduct = HistoryProduct.objects.create(
                user=self.request.user,
                product=product
            )
        
        context['review_add_form'] = review_add_form
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        return context
