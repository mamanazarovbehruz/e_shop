from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.db.models import Count, Sum
# Create your views here.


def product(request):
    products = Product.objects.annotate(
        product_count=Sum('items__count_in_stock')
    )
    
    for product in products:
        if str(product.id) in request.GET:
            product.delete()
    
    products = Product.objects.annotate(
        product_count=Sum('items__count_in_stock')
    )

    return render(request, 'dashboard/products.html', {'products': products})

def productCreate(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            name = product_form.cleaned_data.get('name')
            product_form.save()
            messages.success(request, f'{name} product create successfully!')
            return redirect('products:product')
        else:
            messages.error(request, product_form.errors)
    else:
        product_form = ProductForm()
    
    return render(request, 'dashboard/productCreate.html', {'product_form': product_form})

def productUpdate(request, slug):
    product = Product.objects.get(slug=slug)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            name = product_form.cleaned_data.get('name')
            product_form.save()
            messages.success(request, f'{name} product update successfully!')
            return redirect('products:product')
        else:
            messages.error(request, product_form.errors)
    else:
        product_form = ProductForm(instance=product)
    
    context = {
        'product': product,
        'product_form': product_form,
    }
    
    return render(request, 'dashboard/productUpdate.html', context)

def productDelete(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if product:
        name = product.name
        product.delete()
        messages.success(request, f'{name} product delete successfully!')
        return redirect('products:product')

    return render(request, 'dashboard/products.html')

def productItem(request):
    productItems = ProductItem.objects.all()

    for productItem in productItems:
        if str(productItem.id) in request.GET:
            productItem.delete()
    
    productItems = ProductItem.objects.all()

    return render(request, 'dashboard/product_item.html', {'productItems': productItems})

def productItemCreate(request):
    if request.method == 'POST':
        productItem_form = ProductItemForm(request.POST, files=request.FILES)
        if productItem_form.is_valid():
            title = productItem_form.cleaned_data.get('title')
            productItem_form.save()
            messages.success(request, f'{title} productItem create successfully!')
            return redirect('products:productItem')
        else:
            messages.error(request, productItem_form.errors)
    else:
        productItem_form = ProductItemForm()
    
    return render(request, 'dashboard/productItem_create.html', {'productItem_form': productItem_form})

def productItemUpdate(request, slug):
    productItem = ProductItem.objects.get(slug=slug)

    if request.method == 'POST':
        productItem_form = ProductItemForm(request.POST, files=request.FILES, instance=productItem)
        if productItem_form.is_valid():
            title = productItem_form.cleaned_data.get('title')
            productItem_form.save()
            messages.success(request, f'{title} productItem update successfully!')
            return redirect('products:productItem')
        else:
            messages.error(request, productItem_form.errors)
    else:
        productItem_form = ProductItemForm(instance=productItem)
    
    context = {
        'productItem': productItem,
        'productItem_form': productItem_form,
    }
    
    return render(request, 'dashboard/productItem_update.html', context)

def productItemDelete(request, slug):
    productItem = get_object_or_404(ProductItem, slug=slug)

    if productItem:
        title = productItem.title
        productItem.delete()
        messages.success(request, f'{title} productItem delete successfully!')
        return redirect('products:productItem')

    return render(request, 'dashboard/product_item.html')

def productColor(request):
    productColors = ProductColor.objects.all()

    for productColor in productColors:
        if str(productColor.id) in request.GET:
            productColor.delete()
    
    productColors = ProductColor.objects.all()

    return render(request, 'dashboard/productColor.html', {'productColors': productColors})

def productColorCreate(request):
    if request.method == 'POST':
        productColor_form = ProductColorForm(request.POST)
        if productColor_form.is_valid():
            name = productColor_form.cleaned_data.get('name')
            productColor_form.save()
            messages.success(request, f'{name} productColor create successfully!')
            return redirect('products:productColor')
        else:
            messages.error(request, productColor_form.errors)
    else:
        productColor_form = ProductColorForm()
    
    return render(request, 'dashboard/productColor_create.html', {'productColor_form': productColor_form})

def productColorUpdate(request, id):
    productColor = ProductColor.objects.get(id=id)

    if request.method == 'POST':
        productColor_form = ProductColorForm(request.POST, files=request.FILES, instance=productColor)
        if productColor_form.is_valid():
            name = productColor_form.cleaned_data.get('name')
            productColor_form.save()
            messages.success(request, f'{name} productColor update successfully!')
            return redirect('products:productColor')
        else:
            messages.error(request, productColor_form.errors)
    else:
        productColor_form = ProductColorForm(instance=productColor)
    
    context = {
        'productColor': productColor,
        'productColor_form': productColor_form,
    }
    
    return render(request, 'dashboard/productColor_update.html', context)

def productColorDelete(request, id):
    productColor = get_object_or_404(ProductColor, id=id)

    if productColor:
        name = productColor.name
        productColor.delete()
        messages.success(request, f'{name} productColor delete successfully!')
        return redirect('products:productColor')

    return render(request, 'dashboard/productColor.html')

def productSize(request):
    productSizes = ProductSize.objects.all()

    for productSize in productSizes:
        if str(productSize.id) in request.GET:
            productSize.delete()
    
    productSizes = ProductSize.objects.all()

    return render(request, 'dashboard/productSize.html', {'productSizes': productSizes})

def productSizeCreate(request):
    if request.method == 'POST':
        productSize_form = ProductSizeForm(request.POST)
        if productSize_form.is_valid():
            name = productSize_form.cleaned_data.get('name')
            productSize_form.save()
            messages.success(request, f'{name} productSize create successfully!')
            return redirect('products:productSize')
        else:
            messages.error(request, productSize_form.errors)
    else:
        productSize_form = ProductSizeForm()
    
    return render(request, 'dashboard/productSize_create.html', {'productSize_form': productSize_form})

def productSizeUpdate(request, id):
    productSize = ProductSize.objects.get(id=id)

    if request.method == 'POST':
        productSize_form = ProductSizeForm(request.POST, instance=productSize)
        if productSize_form.is_valid():
            name = productSize_form.cleaned_data.get('name')
            productSize_form.save()
            messages.success(request, f'{name} productSize update successfully!')
            return redirect('products:productSize')
        else:
            messages.error(request, productSize_form.errors)
    else:
        productSize_form = ProductColorForm(instance=productSize)
    
    context = {
        'productSize': productSize,
        'productSize_form': productSize_form,
    }
    
    return render(request, 'dashboard/productSize_update.html', context)

def productSizeDelete(request, id):
    productSize = get_object_or_404(ProductSize, id=id)

    if productSize:
        name = productSize.name
        productSize.delete()
        messages.success(request, f'{name} productSize delete successfully!')
        return redirect('products:productSize')

    return render(request, 'dashboard/productSize.html')

def brand(request):
    brands = Brand.objects.all()

    for brand in brands:
        if str(brand.id) in request.GET:
            brand.delete()
    
    brands = Brand.objects.all()

    return render(request, 'dashboard/brand.html', {'brands': brands})

def brandCreate(request):
    if request.method == 'POST':
        brand_form = BrandForm(request.POST, files=request.FILES)
        if brand_form.is_valid():
            name = brand_form.cleaned_data.get('name')
            brand_form.save()
            messages.success(request, f'{name} brand create successfully!')
            return redirect('products:brand')
        else:
            messages.error(request, brand_form.errors)
    else:
        brand_form = BrandForm()
    
    return render(request, 'dashboard/brand_create.html', {'brand_form': brand_form})

def brandUpdate(request, slug):
    brand = Brand.objects.get(slug=slug)

    if request.method == 'POST':
        brand_form = BrandForm(request.POST, files=request.FILES, instance=brand)
        if brand_form.is_valid():
            name = brand_form.cleaned_data.get('name')
            brand_form.save()
            messages.success(request, f'{name} brand update successfully!')
            return redirect('products:brand')
        else:
            messages.error(request, brand_form.errors)
    else:
        brand_form = BrandForm(instance=brand)
    
    context = {
        'brand': brand,
        'brand_form': brand_form,
    }
    
    return render(request, 'dashboard/brand_update.html', context)

def brandDelete(request, slug):
    brand = get_object_or_404(Brand, slug=slug)

    if brand:
        name = brand.name
        brand.delete()
        messages.success(request, f'{name} brand delete successfully!')
        return redirect('products:brand')

    return render(request, 'dashboard/brand.html')

def category(request):
    categorys = Category.objects.all()

    for category in categorys:
        if str(category.id) in request.GET:
            category.delete()
    
    categorys = Category.objects.all()

    return render(request, 'dashboard/category.html', {'categorys': categorys})

def categoryCreate(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, files=request.FILES)
        if category_form.is_valid():
            title = category_form.cleaned_data.get('title')
            category_form.save()
            messages.success(request, f'{title} category create successfully!')
            return redirect('products:category')
        else:
            messages.error(request, category_form.errors)
    else:
        category_form = CategoryForm()
    
    return render(request, 'dashboard/category_create.html', {'category_form': category_form})

def categoryUpdate(request, slug):
    category = Category.objects.get(slug=slug)

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, files=request.FILES, instance=category)
        if category_form.is_valid():
            title = category_form.cleaned_data.get('title')
            category_form.save()
            messages.success(request, f'{title} category update successfully!')
            return redirect('products:category')
        else:
            messages.error(request, category_form.errors)
    else:
        category_form = CategoryForm(instance=category)
    
    context = {
        'category': category,
        'category_form': category_form,
    }
    
    return render(request, 'dashboard/category_update.html', context)

def categoryDelete(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if category:
        title = category.title
        category.delete()
        messages.success(request, f'{title} category delete successfully!')
        return redirect('products:category')

    return render(request, 'dashboard/category.html')


@login_required
def productCommet(request, slug):
    product = Product.objects.get(slug=slug)

    user = User.objects.get(username=request.user.username)
    data = request.POST.copy()
    data.update({'user': user, 'product': product})
    form = ProductCommentForm(data=data)
    if form.is_valid():
        form.user = user
        form.product = product
        form.save()

    star = request.POST.get('rating')
    if star:
        try:
            st = ProductStar.objects.get(author=user)
            st.percent = star
            st.save()
        except Exception as e:
            ProductStar.objects.create(product=product, author=user, percent=star)
    
    return redirect('general:product_detail', slug)