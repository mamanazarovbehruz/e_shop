from django.db import models
from .servises import *
from accounts.models import User, UserDataOnDelete
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from accounts.validators import is_client, is_admin
from .emums import ProductStars
from django.template.defaultfilters import slugify
from uuid import uuid4
from django_resized import ResizedImageField
from sorl.thumbnail import ImageField, get_thumbnail
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    brand = models.ForeignKey("Brand", on_delete=models.PROTECT)
    author = models.ForeignKey(User, validators=[is_admin], related_name='product_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})
    
    def get_first_item(self):
        item = self.items.first()
        return item

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{uuid4()} {self.name}') 
        super().save(*args, **kwargs)

class ProductItem(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.PROTECT)
    author = models.ForeignKey(User, validators=[is_admin], related_name='productItem_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    size = models.ForeignKey("ProductSize", on_delete=models.PROTECT)
    color = models.ForeignKey("ProductColor", on_delete=models.PROTECT)
    count_in_stock = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = ImageField(upload_to=upload_protuctItem_path)
    image_small = models.ImageField(upload_to=upload_protuctItem_small, blank=True)
    image_medium = models.ImageField(upload_to=upload_protuctItem_path, blank=True)
    image_large = models.ImageField(upload_to=upload_protuctItem_path, blank=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(f'{uuid4()} {self.title}')
        super(ProductItem, self).save(*args, **kwargs)
        self.image_small = get_thumbnail(self.image, '50x60', crop='top', quality=99, format='JPEG').url
        self.image_medium = get_thumbnail(self.image, '286x290', crop='top', quality=99, format='JPEG').url
        self.image_large = get_thumbnail(self.image, '500x550',crop='top', quality=99, format='JPEG').url
        super(ProductItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})


class ProductColor(models.Model):

    name = models.CharField(max_length=20, unique=True, db_index=True)
    color = ColorField(default='#FF0000')
    author = models.ForeignKey(User, validators=[is_admin], related_name='producColor_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

class ProductSize(models.Model):

    name = models.CharField(max_length=50)
    size = models.CharField(max_length=10, unique=True)
    author = models.ForeignKey(User, validators=[is_admin], related_name='productSize_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.size
    
    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})
    
    def save(self, *args, **kwargs):
        self.size = self.size.upper()
        super().save(*args, **kwargs)


class ProductStar(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='productStar_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    percent = models.PositiveSmallIntegerField()

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    parent = models.OneToOneField('self', on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=300)

class ProductItemHistory(models.Model):
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    author = models.ForeignKey(User, validators=[is_admin], related_name='productHistory_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, validators=[is_admin], related_name='brand_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    image = ResizedImageField(
        size=[100, 100],
        scale=0.5, quality=75, upload_to=upload_brand_path)

    def __str__(self) -> str:
        return self.name
    
    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{uuid4} {self.name}')
        super().save(*args, **kwargs)

class Category(models.Model):
    title = models.CharField(max_length=250, unique=True, db_index=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.ForeignKey(User, validators=[is_admin], related_name='category_user', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    image = ImageField(upload_to=upload_category_path)

    def __str__(self):
        return self.title

    def clean(self):
        if self.author and self.author_data:
            raise ValidationError({'{author_data}': 'Filling is not required'})

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{uuid4} {self.title}')
        super().save(*args, **kwargs)
        self.image = get_thumbnail(self.image, '290x300', crop='top', quality=99, format='JPEG').url
        super().save(*args, **kwargs)