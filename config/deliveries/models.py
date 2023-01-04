from django.db import models
from accounts.models import User, UserDataOnDelete
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Delivery(models.Model):

    CHOICES_STATUS = (
        ('warehouse', 'WAREHOUSE'),
        ('packaging', 'PACKAGING'),
        ('delivering', 'DELIVERING'),
        ('delivered', 'DELIVERED'),
        ('closed', 'CLOSED'),
    )

    supplier_name = models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name='delivery_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)
    delivery_time = models.FloatField(validators=[MinValueValidator(1.0)])
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=CHOICES_STATUS[0][0])
    
    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required!'})

    def __str__(self) -> str:
        return self.supplier_name