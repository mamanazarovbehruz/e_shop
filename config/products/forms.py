from django import forms
from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'category', 'brand', 'author', 'description', 'is_active')

class ProductItemForm(forms.ModelForm):

    class Meta:
        model = ProductItem
        fields = ('title', 'product', 'author', 'price', 'size', 'color', 'count_in_stock', 'is_active', 'image')

class ProductColorForm(forms.ModelForm):

    class Meta:
        model = ProductColor
        fields = ('name', 'color', 'author')

class ProductSizeForm(forms.ModelForm):

    class Meta:
        model = ProductSize
        fields = ('name', 'size', 'author')

class ProductCommentForm(forms.ModelForm):

    class Meta:
        model = ProductComment
        fields = ('text', 'user', 'product')

class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ('name', 'author', 'description', 'image')

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title', 'author', 'description', 'is_active', 'image')
