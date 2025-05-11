from django.shortcuts import render,redirect,get_object_or_404
from .models import Restaurant, Deal, Cuisine,OTP,MenuItem
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import SignupForm, OTPForm
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from food.models import Profile

def home(request):
    return render(request,template_name='htmlpages\home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()

            # Create an OTP for email verification
            otp = OTP.objects.create(user=user)

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp.otp_code}. It expires in 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect('verify', user_id=user.id)  # Redirect to OTP verification page
    else:
        form = SignupForm()

    return render(request, 'htmlpages/signup.html', {'form': form})


def verify(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            otp = OTP.objects.filter(user=user, otp_code=otp_code).first()

            if otp and not otp.is_expired():
                user.email_verified = True  # Mark the user as email verified
                user.save()
                otp.delete()  # OTP is used, delete it

                return redirect('confirmation')  # Redirect to confirmation page
            else:
                return render(request, r'htmlpages/verify.html', {'form': form, 'error': 'Invalid or expired OTP.'})
    else:
        form = OTPForm()

    return render(request, r'htmlpages/verify.html', {'form': form, 'user_id': user_id})

def confirmation(request):
    return render(request, template_name='htmlpages/confirmation.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
        else:
            return render(request, 'htmlpages/signin.html', {'error': 'Invalid username or password.'})

    return render(request, 'htmlpages/signin.html')

def dashboard(request):
    featured_restaurants = Restaurant.objects.filter(is_featured=True)
    all_restaurants = Restaurant.objects.all()
    cuisines = Cuisine.objects.all()
    deals = Deal.objects.all()

    context = {
        'featured_restaurants': featured_restaurants,
        'all_restaurants': all_restaurants,
        'cuisines': cuisines,
        'deals': deals
    }
    return render(request, 'htmlpages/dashboard.html', context)

def search(request):
    query = request.GET.get('q')
    results = Restaurant.objects.filter(name__icontains=query) if query else []
    return render(request, 'htmlpages/search.html', {'results': results, 'query': query})

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'htmlpages/restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })

def cart(request):
    return render(request,template_name='htmlpages\cart.html')

def checkout(request):
    return render(request,template_name='htmlpages\checkout.html')

def order_confirmation(request):
    return render(request,template_name='htmlpages\order_confirmation.html')

def profile(request):
    return render(request,template_name='htmlpages\profile.html')

def history(request):
    return render(request,template_name='htmlpages\history.html')




@login_required
def payment(request):
    # Ensure profile exists
    Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bkash = request.POST.get('bkash_number', '').strip()
        nagad = request.POST.get('nagad_number', '').strip()

        if not bkash and not nagad:
            messages.error(request, "Please enter either Bkash or Nagad number.")
            return redirect('payment')

        def is_valid(number):
            return re.fullmatch(r'01\d{9}', number) is not None

        if bkash and not is_valid(bkash):
            messages.error(request, "Bkash number must start with 01 and be 11 digits.")
            return redirect('payment')

        if nagad and not is_valid(nagad):
            messages.error(request, "Nagad number must start with 01 and be 11 digits.")
            return redirect('payment')

        profile = request.user.profile
        profile.bkash_number = bkash if bkash else None
        profile.nagad_number = nagad if nagad else None
        profile.save()

        messages.success(request, "Payment information saved!")
        return redirect('dashboard')

    return render(request, 'htmlpages\payment.html')


def notification(request):
    return render(request,template_name=r'htmlpages\notification.html')

def services(request):
    return render(request,template_name='htmlpages\services.html')

def contact(request):
    return render(request,template_name='htmlpages\contact.html')

def logout_confirm(request):
    return render(request, 'htmlpages/logout.html')
def logout_view(request):
    auth_logout(request)  # This logs the user out
    return redirect('signin')  # 'signin' should match your URL name








