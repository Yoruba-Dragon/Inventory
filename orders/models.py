from django.db import models
from django.conf import settings
from users.models import Products
from django.shortcuts import  redirect

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    quantity = models.PositiveIntegerField()
    notified = models.BooleanField(default=False)  # Track if the user has been notified
    def can_approve(self):
        """Check if the order can be approved based on product availability."""
        return self.product.product_quantity >= self.quantity
    
    def save(self, *args, **kwargs):
        # Handle stock rejection logic
        if self.quantity > self.product.product_quantity:
            self.status = 'Rejected'
       

       

        # Save the updated order
        if self.pk:  # Ensure it's an update, not a new instance
            original = Order.objects.get(pk=self.pk)
            if original.status != self.status and self.status != 'pending':
                self.notified = False  # Reset notification if status changes
        else:
            self.notified = True  # New orders don't need a notification
        super().save(*args, **kwargs)

        # Handle stock updates if approved
        if self.status == 'approved' and self.product.product_quantity >= self.quantity:
            self.product.product_quantity -= self.quantity
            self.product.save()

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.status})"
   