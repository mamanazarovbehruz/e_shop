from .models import User
from django.core.exceptions import ValidationError

def is_client(client_id):

    role = User.objects.get(id=client_id).role
    if role != User.CHOICE_ROLE[0][0]:
        raise ValidationError('you are admin!!!')

def is_admin(admin_id):

    role = User.objects.get(id=admin_id).role
    if role != User.CHOICE_ROLE[1][0]:
        raise ValidationError('you are client!!!')