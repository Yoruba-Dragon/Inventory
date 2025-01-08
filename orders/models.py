from django.db import models
from django.conf import settings
from users.models import Products






class Order(models.Model):

    STATUS_CHOICES=(
        ('pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )



    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    status=  models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    quantity= models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.quantity > self.product.product_quantity:
            self.status = 'Rejected'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.status})"

    def can_approve(self):
        return self.product.product_quantity >= self.quantity
# Create your models here.
