from django.db import models
from .servises import upload_avatar_path
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

# Create your models here.

class User(AbstractUser):

    CHOICE_ROLE = (
        ('client', 'CLIENT'),
        ('admin', 'ADMIN'),
    )

    CHOICE_CURRENCY = (
        ('uzs', 'UZS'),
        ('usd', 'USD'),
        ('rub', 'RUB'),
    )

    CHOICE_CITY = (
        ('tashkent', 'TASHKENT'),
        ('surxondaryo', 'SURXONDARYO'),
    )

    CHOICE_REGION = (
        ('olmazor', 'OLMAZOR'),
        ('chilonzor', 'CHILONZOR'),
        ('kumkurgan', 'KUMKURGAN'),
        ('termiz', 'TERMIZ')
    )

    email = models.EmailField('email address', unique=True)
    phonenumber = PhoneNumberField(null=True, blank=True, unique=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, default='profile/defaultadmin/defaultadmin.png')
    user_currency = models.CharField(max_length=3, choices=CHOICE_CURRENCY, default=CHOICE_CURRENCY[0][0])
    about = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=6, choices=CHOICE_ROLE, default=CHOICE_ROLE[0][0])

    # Address

    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=20, choices=CHOICE_CITY)
    region = models.CharField(max_length=100, choices=CHOICE_REGION)
    zip_code = models.PositiveIntegerField(blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True)

    # Card

    card_number = models.PositiveIntegerField(blank=True, null=True)
    card_date = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CHOICE_CURRENCY, default=CHOICE_CURRENCY[0][0])

    def __str__(self):
        return self.username
    
class UserDataOnDelete(models.Model):
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    username = models.CharField(max_length=128)
    role = models.CharField(max_length=6, choices=User.CHOICE_ROLE, default=User.CHOICE_ROLE[0][0])

    def __str__(self) -> str:
        return self.username