from django.db import models
from accounts.models import User, UserDataOnDelete
from products.models import ProductItem
from django.core.exceptions import ValidationError

# Create your models here.

class Discount(models.Model):
    
    CHOICE_TYPE = (
        ('price', 'PRICE'),
        ('percent', 'PERCENT'),
    )

    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, related_name='discount_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    discount_type = models.CharField(max_length=10, choices=CHOICE_TYPE, default=CHOICE_TYPE[1][0])
    type_sum = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

    def __str__(self) -> str:
        return self.title
    


class DiscountItem(models.Model):
    description = models.CharField(max_length=250, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
    product = models.ForeignKey(ProductItem, on_delete=models.PROTECT)
    author = models.ForeignKey(User, related_name='discountItem_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

    def __str__(self) -> str:
        return self.discount.title
