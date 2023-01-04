from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q
from .forms import *
from .models import User
from django.core.files import File
from django.conf import settings


# Create your views here.

def user_register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password1 = form.cleaned_data.get('password1')

            user = User.objects.filter(Q(username=username) | Q(email=email))
            
            if not user:
                if password == password1:
                    user = User(username = username, email=email)
                    user.set_password(password)
                    user.save()
                    return redirect('accounts:user_login')
                else:
                    messages.error(request, 'The password is not the same')
            else:
                messages.error(request, 'You are registered')
        else:
            messages.error(request, 'The form was filled in incorrectly')
    else:
        form = UserRegisterForm

    return render(request, 'sign_up.html', {'form':form})


def user_login(request):
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid() and form.user_auth():
            user = form.user_auth()
            login(request, user)
            return redirect('general:home')
        else:
            if form.errors:
                messages.error(request, form.errors)
            else:
                messages.error(request, 'You are not registered')
    else:
        form = UserLoginForm()

    return render(request, 'sign_in.html', {'form':form})


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset/password_reset_email.txt"
                    context = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'e_shop',
                        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user':user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject ,email, 'mbpy2000@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found')
                    return redirect('/password_reset/done/')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name='password_reset/password_reset.html', context={'password_reset_form':password_reset_form})


def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


def dashboard(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'dashboard/dashboard_index.html', context)


def dashboard_clients(request):

    users = []
    for user in User.objects.all():
        if user.role == 'client':
            users.append(user)
    context = {
        'users': users,
    }

    return render(request, 'dashboard/clients.html', context)

def user_role(request, pk):
    user1 = User.objects.get(id=pk)
    users = []
    form = UserRoleForm()
    for user in User.objects.all():
        if user.role == 'client':
            users.append(user)

    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user1)
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard_clients')
        else:
            messages.error(request, form.errors)
    
    context = {
        'user1':user1,
        'form':form,
        'users': users,
    }

    return render(request, 'dashboard/clients.html', context)

def profile_home(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'profile/user_profile_index.html', context)


@login_required(login_url='accounts:user_login')
def profile(request):

    user = request.user
    currency_form = UserCurrencyForm(instance=user)
    card_form = UserCardChangeForm(instance=user)
    pass_form = UserChangePassword()
    address_form = UserAddressForm(instance=user)

    context = {
            'user': user,
            'card_form': card_form,
            'currency_form': currency_form,
            'pass_form': pass_form,
            'address_form': address_form,
        }

    return render(request, 'profile/user_profile.html', context)


def profile_update(request, pk):
    form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            
    if form.is_valid():
        user = form.save(commit=False)
        if request.POST.get('delete_avatar'):
            form.cleaned_data['avatar'] = None
            user.avatar.save(
                'defaultadmin.png', File(open(settings.DEFAULT_AVATAR_URL, 'rb'))
            )
        user.save()
    else:
        messages.error(request, form.errors)

    return redirect('accounts:profile')


def user_change_card(request, pk):

    card1_form = UserCardChangeForm(request.POST, instance=request.user)
    if card1_form.is_valid():
        card1_form.save()
        messages.success(request, 'Card information has changed')
    else:
        messages.error(request, card1_form.errors)
    
    return redirect('accounts:profile')


def user_change_password(request, pk):
    
    pass_form = UserChangePassword(request.POST)
    if pass_form.is_valid():
        user = User.objects.get(username=request.user)
        if user.check_password(pass_form.cleaned_data['password']):
            if pass_form.cleaned_data['password1'] == pass_form.cleaned_data['password2']:
                user.set_password(pass_form.cleaned_data['password2'])
                user.save()
                messages.success(request, 'Password changed successfully!')
            else:
                messages.error(request, 'New passwords don\'t similar!')
        else:
            messages.error(request, 'The old password was entered incorrectly!')
    else:
        messages.error(request, pass_form.errors)
    
    return redirect('accounts:profile')


def user_change_address(request, pk):

    address_form = UserAddressForm(request.POST, instance=request.user)
    if address_form.is_valid():
        address_form.save()
        messages.success(request, 'Address changed successfully')
    else:
        messages.error(request, address_form.errors)
    
    return redirect('accounts:profile')



def user_delete(request, pk):
    
    user = get_object_or_404(User, id=pk)
    if request.POST:
        user.delete()
        return redirect('general:home')

    return render(request, 'user_delete.html')