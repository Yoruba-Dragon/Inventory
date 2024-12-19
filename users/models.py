from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



CATEGORY1=(
    ("Operations","Operations"),
    ("Strategy","Strategy"),
    ("Credit","Credit"),
    ("Human Resource","Human Resource"),
    ("Sales","Sales"),
    ("Finance","Finance"),
    ("Communictions and Marketing","Communications and Marketing"),
    ("Internal control and compliance","Internal control and compliance"),
    ("Facility","Facility"),
)

CATEGORY2=(

    ("Stationary","Stationary"),
    ("Office Equipment","Office Equipment"),
    ("Clothes","Clothes"),
 )

class UserProfile(models.Model):
    first_name= models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=50, choices=CATEGORY1, null=True)
    picture = models.ImageField(upload_to="Pictures")
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True)
      
    
    @receiver(post_save, sender=User)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
    def __str__(self):
        return f"UserProfile of {self.user.username}"


class Products(models.Model):
    product_name = models.CharField(max_length=50, null=True)
    product_description = models.CharField(max_length=200, null=True)
    product_quantity= models.IntegerField()
    category= models.CharField(max_length=50, choices= CATEGORY2, null=True)
    def __str__(self):
        return f"Product of {self.product_name}"

# Create your models here.
