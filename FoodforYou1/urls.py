"""
URL configuration for FoodforYou1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


from food import views as food_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',food_views.home, name='home'),
    path('signup/',food_views.signup, name='signup'),
    path('verify/<int:user_id>/',food_views.verify, name='verify'),
    path('confirmation/',food_views.confirmation, name='confirmation'),
    path('signin/', food_views.signin, name='signin'),
    path('dashboard/',food_views.dashboard, name='dashboard'),
    path('search/',food_views.search, name='search'),
    path('restaurant/<int:id>/',food_views.restaurant_detail, name='restaurant_detail'),
    path('cart/',food_views.cart, name='cart'),
    path('checkout/',food_views.checkout, name='checkout'),
    path('order_confirmation/',food_views.order_confirmation, name='order_confirmation'),
    path('profile/',food_views.profile, name='profile'),
    path('history/',food_views.history, name='history'),
    path('payment/',food_views.payment, name='payment'),
    path('notification/',food_views.notification, name='notification'),
    path('services/',food_views.services, name='services'),
    path('contact/',food_views.contact, name='contact'),
path('logout/', food_views.logout_confirm, name='logout'),  # Goes to confirmation page
    path('logout/confirm/', food_views.logout_view, name='logout_confirm'),
    path('logout/',food_views.logout_view, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)