from django.contrib import admin

# Register your models here.
from app_cart.models import CartDatabase


@admin.register(CartDatabase)
class CartDatabaseAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in CartDatabase._meta.get_fields()
    ]