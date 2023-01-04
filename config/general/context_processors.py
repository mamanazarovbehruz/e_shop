from products.models import Category
from wishlists.models import Wishlist

def category_for_context(request):
    category = Category.objects.all()

    w_count = 0
    if request.user.is_authenticated:
        user = request.user
        wishlist = Wishlist.objects.filter(client=user)
        if wishlist:
            w_count = wishlist.count()

    ins = 0
    if 'cart' in request.session:
        card = request.session['cart']
        for i in card:
            ins += 1

    return {'category': category, 'w_count': w_count, 'ins': ins}