from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, fullname, password, **extra_fields)

CATEGORY1 = (
    ("Operations", "Operations"),
    ("Strategy", "Strategy"),
    ("Credit", "Credit"),
    ("Human Resource", "Human Resource"),
    ("Sales", "Sales"),
    ("Finance", "Finance"),
    ("Communications and Marketing", "Communications and Marketing"),
    ("R.C.C", "R.C.C"),
    
)

CATEGORY2 = (
    ("Stationary", "Stationary"),
    ("Office Equipment", "Office Equipment"),
    ("Clothes", "Clothes"),
)
class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=150, verbose_name="Full Name")  # New field for full name
    email = models.EmailField(unique=True)  # Use email as the login field
    username = None  # Remove the default username field
    department = models.CharField(
        max_length=50,
        choices=CATEGORY1,
    )
    picture = models.ImageField(upload_to="Pictures", blank=True, null=True)

    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = ['fullname']  # Full name is required during signup

    objects = CustomUserManager()  # Use the custom manager

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

class Products(models.Model):
    product_name = models.CharField(max_length=50, null=True)
    product_description = models.CharField(max_length=200, null=True)
    product_quantity = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY2, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


