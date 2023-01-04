from django import forms
from .models import *

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        field = ('title', 'author', 'delivery', 'closed_date', 'shipping_address1', 'is_confirmed', 'is_success', 'total_price')

class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        field = ('product_item', 'order', 'count', 'author', 'price')

class OrderPaymentForm(forms.ModelForm):

    class Meta:
        model = OrderPayment
        field = ('order', 'client', 'payment_type', 'payed')