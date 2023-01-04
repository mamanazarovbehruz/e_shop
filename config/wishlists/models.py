from django.db import models
from accounts.models import User, UserDataOnDelete
from products.models import ProductItem
from accounts.validators import is_client
from django.core.exceptions import ValidationError

# Create your models here.

class Wishlist(models.Model):

    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    client = models.ForeignKey(User, validators=[is_client], related_name='wishlist_client', on_delete=models.CASCADE)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

    class Meta:
        unique_together = ['product', 'client']