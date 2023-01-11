from django.shortcuts import render, redirect
from account.forms import *
from payment.forms import ShippingForm
from django.contrib.sites.shortcuts import get_current_site
from account.token import user_token_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from account.models import UserCart
from payment.models import ShippingAddress

@user_passes_test(lambda u : u.is_anonymous, login_url='store:store')
def signup(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('account/signup/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_token_generate.make_token(user),
            })

            user.email_user(subject=subject, message='', html_message=message)

            request.session['redirect'] = True
            return redirect('account:email_verification_sent')

        error_found = False

        for field in form:
            for error in field.errors:
                error_found = True
                messages.add_message(request, messages.ERROR, error)

            if error_found:
                break

        return redirect('account:signup')

    return render(request, 'account/signup/signup.html', context={'title': 'Product Destination | Sign Up', 'form': form})

@user_passes_test(lambda u : u.is_anonymous, login_url='store:store')
def signin(request):
    form = SignInForm()

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                try:
                    user_cart = UserCart.objects.get(username=username)
                    request.session['cart'] = user_cart.user_cart
                    request.session['total'] = float(user_cart.total)
                except:
                    UserCart.objects.create(username=username)
                    UserCart.objects.filter(username=username).update(user_cart=request.session['cart'], total=request.session['total'])

                auth.login(request, user)
                return redirect('store:store')
            else:
                return redirect('account:signin')

        messages.error(request, form.non_field_errors())
        return redirect('account:signin')

    return render(request, 'account/signin/signin.html', context={'title': 'Product Destination | Sign In', 'form': form})

@login_required(login_url='account:signin')
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'Logout success')
    return redirect('account:signin')

def email_verification_sent(request):
    if 'redirect' not in request.session:
        return redirect('store:store')

    del request.session['redirect']
    return render(request, 'account/signup/email_verification_sent.html', context={'title': 'Email Verification Sent'})

def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user and user_token_generate.check_token(user, token):
        user.is_active = True
        user.save()
        request.session['redirect'] = True
        return redirect('account:email_verification_success')

def email_verification_success(request):
    if 'redirect' not in request.session:
        return redirect('store:store')

    del request.session['redirect']
    return render(request, 'account/signup/email_verification_success.html', context={'title': 'Email Verified Successfully'})

@login_required(login_url='account:signin')
def profile(request):
    user_form = UserUpdateForm(instance=request.user)

    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except:
        shipping = None

    shipping_form = ShippingForm(instance=shipping)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            return redirect('account:profile')

    return render(request, 'account/profile.html', context={'title': 'Profile', 'form': user_form, 'shipping_form': shipping_form})

@login_required(login_url='account:signin')
def delete_account(request):
    User.objects.get(username=request.user.username).delete()
    UserCart.objects.get(username=request.user.username).delete()
    request.session.flush()
    return redirect('account:signup')

@login_required(login_url='account:signin')
def manage_shipping(request):
    if request.method == "POST":
        try:
            shipping = ShippingAddress.objects.get(user=request.user.id)
        except:
            shipping = None

        shipping_form = ShippingForm(request.POST, instance=shipping)

        if shipping_form.is_valid():
            shipping_user = shipping_form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()

            messages.error(request, 'Shipping details updated successfully.')
            return redirect('account:profile')

        error_found = False

        for field in shipping_form:
            for error in field.errors:
                error_found = True
                messages.add_message(request, messages.ERROR, error)

            if error_found:
                break

        return redirect('account:profile')

    return redirect('account:profile')