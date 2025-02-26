from django.db import models

# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Advertisement(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    text = models.CharField(max_length=160)
    category = models.CharField(max_length=50, choices=[('fashion', 'Fashion'), ('food', 'Food'), ('electronics', 'Electronics')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
