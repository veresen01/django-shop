from django.contrib import admin

# Register your models here.
from app_reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'user',
        'create_at',
        'text'
    ]
