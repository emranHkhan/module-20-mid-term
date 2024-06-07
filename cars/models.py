from django.db import models
from django.contrib.auth.models import User
from brands.models import Brand

class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return f"{self.name}"
    

class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')

    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Commented by {self.name}"

