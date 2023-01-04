from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.contrib import messages
from decimal import Decimal
from deliveries.models import Delivery


from accounts.models import User
from .models import ShopAbout, ContactUs, ContactQuery
from products.models import *

# Create your views here.
@login_required
def home(request):
    user = request.user
    
    products = Product.objects.all()
    context = {
        'user': user,
        'products': products,
    }

    return render(request, 'index.html', context)

def shop(request):

    productItems = ProductItem.objects.all().order_by('price')
    total_count = productItems.aggregate(total_count=Sum('count_in_stock'))['total_count']

    colors = ProductColor.objects.annotate(
        product_count=Sum('productitem__count_in_stock'),
    )

    sizes = ProductSize.objects.annotate(
        product_count=Sum('productitem__count_in_stock'),
    )

    # Filter products

    request.session['filter'] = {}
    request.session['product_name'] = {}
    if bool(request.GET):
        for x, y in request.GET.items():
            if y == 'on' and x not in request.session['filter']:
                request.session['filter'][str(x)] = True

        if 'all_price' in request.GET:
            productItems = set(filter(lambda obj: obj.price, productItems))
        else:
            productitem = set()
            if '0_price_100' in request.GET:
                productitem = set(filter(lambda obj: 0 <= obj.price <= 100, productItems))
            if '100_price_200' in request.GET:
                productitem = set(filter(lambda obj: 100 <= obj.price <= 200, productItems)) | productitem
            if '200_price_300' in request.GET:
                productitem = set(filter(lambda obj: 200 <= obj.price <= 300, productItems)) | productitem
            if '300_price_400' in request.GET:
                productitem = set(filter(lambda obj: 300 <= obj.price <= 400, productItems)) | productitem
            if '400_price_more' in request.GET:
                productitem = set(filter(lambda obj: 400 <= obj.price, productItems)) | productitem
            productItems = productitem
        

        if 'all_color' in request.GET:
            productItems = set(filter(lambda obj: obj.color, productItems))
        else:
            cs = []
            for c in colors:
                if f'{c.name}' in request.GET:
                    cs.append(c.name)
            productItems = set(filter(lambda obj: obj.color.name in cs, productItems))
        
        if 'all_size' in request.GET:
            productItems = set(filter(lambda obj: obj.size, productItems))
        else:
            ss = []
            for s in sizes:
                if f'{s.size}' in request.GET:
                    ss.append(s.size)
            productItems = set(filter(lambda obj: obj.size.size in ss, productItems))
        

    # data_in_cashe = cache.get('productItems', False)
    # if not data_in_cashe:
    #     productItems = cache.set('productItems', productItems)

    productItems = list(productItems)
    productItems.sort(key=lambda obj: obj.price)
    for product in productItems:
        request.session['product_name'][str(product.title)] = product.title

    context = {
        'productItems': productItems,
        'colors': colors,
        'sizes': sizes,
        'total_count': total_count,
    }
    return render(request, 'shop.html', context)

def shop_product_search(request):
    productItems = ProductItem.objects.all().order_by('price')
    total_count = productItems.aggregate(total_count=Sum('count_in_stock'))['total_count']

    colors = ProductColor.objects.annotate(
        product_count=Sum('productitem__count_in_stock'),
    )

    sizes = ProductSize.objects.annotate(
        product_count=Sum('productitem__count_in_stock'),
    )
    # Search product
    if request.session['filter']:
        if 'q' in request.GET:
            q_list = []
            q = request.GET['q']
            for title in request.session['product_name']:
                if q.lower() in title.lower():
                    q_list.append(title)
            productItems = set(filter(lambda obj: obj.title in q_list, productItems))
    else:
        print('salom1')
        if 'q' in request.GET:
            q = request.GET['q']
            productItems = ProductItem.objects.filter(title__icontains=q)
    
    productItems = list(productItems)
    productItems.sort(key=lambda obj: obj.price)

    context = {
        'productItems': productItems,
        'colors': colors,
        'sizes': sizes,
        'total_count': total_count,
    }
    return render(request, 'shop.html', context)

def product_search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))

        if data and q:
            data_q = 'True'
        elif data:
            data_q = 'TrueFalse'
        else:
            data_q = 'False'
    
    context = {
        'q': q,
        'data': data,
        'data_q': data_q
    }

    return render(request, 'search_products.html', context)

def category_search(request, slug):
    category_data = Category.objects.get(slug=slug)
    data = Product.objects.filter(category=category_data)

    return render(request, 'search_category.html', {'data': data})

def product_detail(request, slug):
    products = Product.objects.all().order_by('-create')[:10]
    product = Product.objects.filter(slug=slug).prefetch_related(
        'productcomment_set', 'items', 'productstar_set'
    )
    product = product.first()
    commet_count = ProductComment.objects.filter(product=product).count()

    context = {
        'product': product,
        'products': products,
        'commet_count': commet_count,
    }

    return render(request, 'detail.html', context)

def productItem_card(request, slug):
    return render(request, 'card.html')

def card(request):
    if 'cart' in request.session:
        card = request.session['cart']
        total_sum = 0
        for i in card.values():
            total_sum += Decimal(i['total'])
    else:
        total_sum = 0

    return render(request, 'card.html', {'total_sum': total_sum})

def card_add(request, slug, quantity):

    if 'quantity' in request.GET:
        quantity = request.GET['quantity']

    productitem = ProductItem.objects.get(slug=slug)
    if not request.session.get('cart'):
        request.session['cart'] = {}
    cart = request.session['cart']
    if not cart.get(str(productitem.id)):
        cart[str(productitem.id)] = {'quantity': 0, 'id': productitem.id, 
            'price': str(productitem.price), 'title': productitem.title, 'total': 0}
        request.session.modified = True
    
    if quantity:
        cart[str(productitem.id)]['quantity'] += int(quantity)
        cart[str(productitem.id)]['total'] = str(productitem.price * int(quantity))
    else:
        cart[str(productitem.id)]['quantity'] += 1
        cart[str(productitem.id)]['total'] = str(productitem.price)
        request.session.modified = True

    return redirect(request.META['HTTP_REFERER'])

def card_update(request, id):
    productitem = ProductItem.objects.get(id=id)
    quantity = 0
    if 'quantity' in request.GET:
        quantity = request.GET['quantity']
    cart = request.session['cart']
    cart[str(productitem.id)]['quantity'] = int(quantity)
    cart[str(productitem.id)]['total'] = str(productitem.price * int(quantity))
    request.session.modified = True
    return redirect('general:card')

def card_remove(request, id):
    productitem = ProductItem.objects.get(id=id)
    cart = request.session['cart']
    if str(productitem.id) in cart:
        del cart[str(productitem.id)]
    request.session.modified = True
    return redirect('general:card')

def card_clear(request):
    # remove cart from session
    del request.session['cart']
    request.session['cart'] = {}
    return redirect('general:card')

def checkout(request):

    delivery = Delivery.objects.first()
    shipping = delivery.price

    card = request.session['cart']
    total_sum = 0
    for i in card.values():
        total_sum += Decimal(i['total'])
    
    total = shipping + total_sum

    context = {
        'total_sum': total_sum,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'checkout.html', context)

def contact(request):
    shopabout = ShopAbout.objects.first()
    contactus = ContactUs.objects.all()

    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('username')).first()
        if user:
            if user.email == request.POST.get('email'):
                contactquery = ContactQuery(
                    username=request.POST.get('username'),
                    email=request.POST.get('email'),
                    subject=request.POST.get('subject'),
                    text=request.POST.get('text'),
                )
                contactquery.save()
                messages.success(request, f'{contactquery.username} send message')
            else:
                messages.error(request, 'email sizga tegishli emas')
        else:
            messages.error(request, 'siz registeratsiyadan otmagansiz')
        
        return redirect('general:contact')
        


    context = {
        'shopabout': shopabout,
        'contactus': contactus,
    }
    return render(request, 'contact.html', context)
