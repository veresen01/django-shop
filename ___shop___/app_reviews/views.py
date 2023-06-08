from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse
from django.views import generic

from app_product.models import Product
from app_reviews.forms import ReviewForm
from app_reviews.models import Review


class AddReview(generic.View):
    def post(self, request: HttpRequest):
        
        if not request.user.is_authenticated:
            raise PermissionDenied()
        
        review_add_form = ReviewForm(request.POST)
        if review_add_form.is_valid():
            product_id = request.POST.get('product_id', None)
            if product_id is not None:
                product = Product.objects.get(pk=product_id)
                new_review: Review = review_add_form.save(commit=False)
                new_review.user = request.user
                new_review.product = product
                new_review.save()
                url = reverse('product:product_detail', kwargs={'pk': product.id})
                return redirect(url + '#reviews')
