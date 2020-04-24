from django.db import models
from usermanagement.models import UserProfile
# Create your models here.
class Shop(models.Model):
    SHOP_CHOICES = [
        ('Grocery', 'Grocery'),
        ('Medical-Store','Medical-Store'),
        ('Food','Food'),
    ]
    shop_name = models.CharField(max_length = 245,unique = True,null = False)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    location = models.CharField(max_length = 245)
    shop_type = models.CharField(max_length = 245 , choices = SHOP_CHOICES,default = 'Grocery')
    def __str__(self):
        return self.shop_name

class Request(models.Model):
    placer = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    expected_going_time = models.TimeField()
    expected_leaving_time = models.TimeField()
    shop_name = models.ForeignKey(Shop,related_name='Shop',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.placer) + str(self.expected_going_time) + str(self.expected_leaving_time) + str(self.shop_name)

class Notifiaction(models.Model):
    status = models.BooleanField(default = False)
    message  = models.CharField(max_length = 254)
    user_prof = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.message
         