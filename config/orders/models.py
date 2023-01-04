from django.db import models
from accounts.models import User, UserDataOnDelete
from products.models import ProductItem
from deliveries.models import Delivery
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.validators import is_client

# Create your models here.

class Order(models.Model):

    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name='order_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True)
    closed_date = models.DateTimeField(blank=True, null=True)
    shipping_address1 = models.CharField(max_length=150)
    is_confirmed = models.BooleanField(default=False)
    is_success = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=13, decimal_places=2)


    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})
    
    def __str__(self):
        return self.title
    

class OrderItem(models.Model):

    product_item = models.ForeignKey(ProductItem, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    author = models.ForeignKey(User, related_name='orderItem_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.price = self.product_item.price

class OrderPayment(models.Model):

    CHOICE_PAYMENT = (
        ('cash', 'CASH'),
        ('plastic_card', 'PLASTIC_CARD'),
        ('coupon', 'COUPON')
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name='orderPayment_user', on_delete=models.SET_NULL, null=True, validators=[is_client])
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    payment_type = models.CharField(max_length=12, choices=CHOICE_PAYMENT, default=CHOICE_PAYMENT[1][0])
    payed = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payed_date = models.DateField(auto_now_add=True)
    debt = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})