from django.contrib import admin
from .models import Discount, DiscountItem

# Register your models here.

admin.site.register(Discount)
admin.site.register(DiscountItem)