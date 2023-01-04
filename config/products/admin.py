from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.ProductItem)
admin.site.register(models.ProductColor)
admin.site.register(models.ProductSize)
admin.site.register(models.ProductStar)
admin.site.register(models.ProductComment)
admin.site.register(models.ProductItemHistory)
admin.site.register(models.Brand)
admin.site.register(models.Category)