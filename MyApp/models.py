from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,related_name='UserProfileInfo',on_delete=models.DO_NOTHING)
    somaiya_id = models.IntegerField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank = True)

    def __str__(self):
        return self.user.username

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# post_save.connect(create_user_profile, sender=User)


    # userid = models.IntegerField(unique=True)
    # password = models.CharField(max_length=264)

    # def __str__(self):
    #     return str(self.userid)

class Product(models.Model):
    product_name = models.CharField(max_length = 256, unique = True)
    product_image =  models.ImageField(upload_to='product_images',blank = True)
    product_cost = models.IntegerField()
    product_available = models.BooleanField(null = True)
    # buyUrl = model.UrlField()
    def __str__(self):
        return self.product_name

# class Order(models.Model):
#     user = models.ForeignKey(User,related_name='User',on_delete=models.DO_NOTHING)
#     product = models.ForeignKey(Product,related_name='Product',on_delete=models.DO_NOTHING,null = True)
#     order_state = models.BooleanField(default = False, null=True)
#     def __str__(self):
#         return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Product, related_name='item', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    total = models.IntegerField()
    order_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user)+ " - " + str(self.order_id)

class Order(models.Model):
    user = models.ForeignKey(User,related_name='User',on_delete=models.DO_NOTHING)
    paymentStatus = models.CharField(max_length = 256, default="Failed")
    orderState = models.BooleanField(default = False, null=True)
    orderTotal = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)
    razorpay_payment_id = models.CharField(max_length = 256)
    razorpay_order_id = models.CharField(max_length = 256)
    razorpay_signature = models.CharField(max_length = 256)
