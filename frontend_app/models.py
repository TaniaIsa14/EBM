import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from tinymce.models import HTMLField

from admin_app.models import Venue
import datetime as dt


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_info")
    phone_number = models.CharField(max_length=11)
    location = models.TextField()


class FrontendInfo(models.Model):
    phone_number = models.IntegerField(verbose_name="Official phone number")
    active_hour = models.CharField(max_length=150, verbose_name="Office active hours")
    first_banner = models.ImageField(verbose_name="Frontend main banner")
    banner_title = models.CharField(max_length=150, verbose_name="Frontend main banner title")
    banner_subtitle = models.CharField(max_length=150, verbose_name="Frontend main banner subtitle")
    description = HTMLField(verbose_name="EBM description")
    login_background = models.ImageField(verbose_name="Login background")
    checkout_background = models.ImageField(verbose_name="Checkout background")
    description_image = models.ImageField(verbose_name="EBM description image")
    description_banner = models.ImageField(verbose_name="EBM description banner")
    location = models.CharField(max_length=150, verbose_name="Office location")
    email = models.EmailField(max_length=150, verbose_name="Office email")
    twitter = models.CharField(verbose_name="Our official twitter", max_length=150)
    facebook = models.CharField(verbose_name="Our official facebook", max_length=150)
    instagram = models.CharField(verbose_name="Our official instagram", max_length=150)
    linkedin = models.CharField(verbose_name="Our official linkedin", max_length=150)
    google_plus = models.CharField(verbose_name="Our official google-plus", max_length=150)


class PackageType(models.Model):
    name = models.CharField(verbose_name="Package type name", max_length=150)

    def human_readable_state(self):
        return self.name.replace('_', ' ')

    def __str__(self):
        return self.name


class Package(models.Model):
    type = models.ForeignKey(PackageType, on_delete=models.CASCADE, related_name="get_package")
    title = models.CharField(verbose_name="Package title", max_length=150)
    subtitle = models.CharField(verbose_name="Package small description", max_length=150)
    description = HTMLField(verbose_name="Package description")
    image = models.ImageField(verbose_name="Package image")
    package_cost = models.DecimalField(verbose_name="Package initial cost", max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Title: {self.title}, Subtitle: {self.subtitle}'


class PackageFood(models.Model):
    religion_choices = [
        ("islam", "Islam"),
        ("hindu", "Hindu"),
        ("christan", "Christan"),
        ("buddha", "Buddha"),
    ]
    package = models.ForeignKey(Package, blank=True, null=True, on_delete=models.CASCADE, related_name="package_foods")
    religion = models.CharField(max_length=150, choices=religion_choices)
    food = models.TextField(verbose_name="Food lists", max_length=150)
    price = models.DecimalField(verbose_name="Price per person", max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Religion: {self.religion}, Food: {self.food}'


class EventsOrganize(models.Model):
    title = models.CharField(verbose_name="Event title", max_length=150)
    description = HTMLField(verbose_name="Event description")
    image = models.ImageField(verbose_name="Event image")
    price = models.PositiveIntegerField(verbose_name="Event price")


class EventBook(models.Model):
    package = models.ForeignKey(Package, blank=True, related_name="package_book", on_delete=models.CASCADE)
    HOUR_CHOICES = [
        (dt.time(hour=10, minute=00), dt.time(hour=10, minute=00)),
        (dt.time(hour=16, minute=00), dt.time(hour=16, minute=00)),
    ]
    package_food = models.ForeignKey(PackageFood, null=True, blank=True, related_name="package_food_related",
                                     on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, related_name="user_book", on_delete=models.CASCADE)
    my_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="venue_book")
    date = models.DateField()
    time = models.TimeField(choices=HOUR_CHOICES, max_length=13)
    people = models.PositiveIntegerField()
    message = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=Decimal(0))
    accept = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = (self.package_food.price * self.people) + self.package.package_cost + self.my_venue.price
        super().save(*args, **kwargs)

    @property
    def is_date_today(self):
        return self.date == datetime.date.today()

    def available_date(self):
        if self.date > datetime.date.today():
            return self.date - datetime.date.today()


class CheckoutInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_checkout')
    event_book = models.ForeignKey(EventBook, on_delete=models.CASCADE, related_name='event_checkout')
    tran_id = models.SlugField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    cart_type = models.CharField(max_length=150)
    transaction_date = models.DateTimeField()
    bank_transaction_id = models.CharField(max_length=150)


class TeamMember(models.Model):
    name = models.CharField(verbose_name="Team member name", max_length=150)
    role = models.CharField(verbose_name="Team member role", max_length=150)
    image = models.ImageField(verbose_name="Team member image")
    twitter = models.CharField(verbose_name="Team member twitter account name", max_length=150)
    facebook = models.CharField(verbose_name="Team member facebook account name", max_length=150)
    instagram = models.CharField(verbose_name="Team member instagram account name", max_length=150)
    linkedin = models.CharField(verbose_name="Team member linkedin account name", max_length=150)


class MessageUs(models.Model):
    name = models.CharField(verbose_name="User name", max_length=150)
    email = models.EmailField(verbose_name="User email")
    subject = models.CharField(verbose_name="Message subject", max_length=150)
    message = models.TextField()
