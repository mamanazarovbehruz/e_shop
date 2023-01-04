from django.shortcuts import render, redirect
from products.models import ProductItem
from .models import Wishlist
from django.contrib import messages

# Create your views here.

def wishlist(request):
    user = request.user
    data = Wishlist.objects.filter(client=user)
    return render(request, 'wishlist.html', {'data': data})

def wishlist_add(request, slug):

    productitem = ProductItem.objects.get(slug=slug)
    user = request.user
    if user.role == 'client':
        wishlist = Wishlist.objects.filter(product=productitem)
        if not wishlist:
            wishlist = Wishlist(
                product=productitem,
                client=user,
            )
            wishlist.save()
        else:
            messages.error(request, 'Bu product wishlistga qo\'shilgan')
    else:
        messages.error(request, 'you are admin')
    return redirect(request.META['HTTP_REFERER'])

def wishlist_delete(request, id):
    wishlist = Wishlist.objects.get(id=id)
    wishlist.delete()
    return redirect('wishlist:wishlist')