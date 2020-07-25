from django.contrib import admin
from MyApp.models import UserProfileInfo,Product,Order, Cart

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
