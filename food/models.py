from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta  
from django.utils import timezone
import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver

class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cuisines/')

    def __str__(self):
        return self.name


class Deal(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='deals/')
    offer_text = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='restaurants/')
    rating = models.FloatField()
    reviews = models.IntegerField()
    delivery_time = models.CharField(max_length=100)
    offer = models.CharField(max_length=100, blank=True)
    cuisine = models.ManyToManyField(Cuisine)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name




# OTP Model
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        self.otp_code = self.generate_otp()
        self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)





class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bkash_number = models.CharField(max_length=11, blank=True, null=True)
    nagad_number = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Automatically create or update the Profile when User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    elif hasattr(instance, 'profile'):
        instance.profile.save()

