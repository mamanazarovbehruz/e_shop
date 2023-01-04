from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class ShopAbout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    create_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class ContactUs(models.Model):
    title = models.CharField(max_length=50)
    shop = models.ForeignKey(ShopAbout, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = PhoneNumberField(unique=True)

    def __str__(self) -> str:
        return self.title
    
class ContactQuery(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=250)
    text = models.TextField()

    def __str__(self):
        return self.subject