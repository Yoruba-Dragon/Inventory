from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    department = models.CharField(
        max_length=50,
        choices=CATEGORY1,
        default="Operations",
    )
    picture = models.ImageField(upload_to="Pictures", blank=True, null=True)

    def __str__(self):
        return self.username

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


