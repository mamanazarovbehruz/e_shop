from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.forms import model_to_dict
from .models import User, UserDataOnDelete

@receiver(pre_delete, sender=User)

def save_user_data_on_delete(instance, *args, **kwargs):

    deliveries = instance.delivery_user.all()
    discounts = instance.discount_user.all()
    discountItems = instance.discountItem_user.all()
    orders = instance.order_user.all()
    orderItems = instance.orderItem_user.all()
    wishlist = instance.wishlist_client.all()
    products = instance.product_user.all()
    productItems = instance.productItem_user.all()
    productColors = instance.productColor_user.all()
    productSizes = instance.productSize_user.all()
    productStars = instance.productStar_user.all()
    productHistories = instance.productHistory_user.all()
    brands = instance.brand_user.all()
    categories = instance.category_user.all()
    
    user_data = UserDataOnDelete.objects.create(
        **model_to_dict(instance, fields=[
            'first_name', 'last_name', 'username', 'role'
        ]))
    
    if deliveries.exists():
        deliveries.update(author_id=user_data.id)
    
    if discounts.exists():
        discounts.update(author_id=user_data.id)
    
    if discountItems.exists():
        discountItems.update(author_id=user_data.id)
    
    if orders.exists():
        orders.update(author_id=user_data.id)
    
    if orderItems.exists():
        orderItems.update(author_id=user_data.id)
    
    if wishlist.exists():
        wishlist.update(author_id=user_data.id)
    
    if products.exists():
        products.update(author_id=user_data.id)
    
    if productItems.exists():
        productItems.update(author_id=user_data.id)
    
    if productColors.exists():
        productColors.update(author_id=user_data.id)
    
    if productSizes.exists():
        productSizes.update(author_id=user_data.id)
    
    if productStars.exists():
        productStars.update(author_id=user_data.id)
    
    if productHistories.exists():
        productHistories.update(author_id=user_data.id)
    
    if brands.exists():
        brands.update(author_id=user_data.id)
    
    if categories.exists():
        categories.update(author_id=user_data.id)