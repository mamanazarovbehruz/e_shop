from django.contrib import admin
from .models import ShopAbout, ContactUs, ContactQuery

# Register your models here.

admin.site.register(ShopAbout)
admin.site.register(ContactUs)
admin.site.register(ContactQuery)