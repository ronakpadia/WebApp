"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from MyApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    re_path(r'^signup/', views.signup, name='signup'),
    re_path(r'login/', views.user_login,name = 'login'),
    re_path(r'^logout/$', views.user_logout, name='logout'),
    re_path(r'^userProfile/$', views.user_profile, name='userProfile'),
    re_path(r'^addProduct/$', views.add_product, name='addProduct'),
    re_path(r'^menu/$', views.menuPage, name='menu'),
    re_path(r'^orders/$', views.ViewOrders, name='ViewOrders'),
    re_path(r'^editProfile/$', views.edit_profile,name='editProfile'),
    re_path(r'^editProduct/(?P<pid>\w{0,50})/$', views.edit_product,name='editProduct'),
    re_path(r'^menu/(?P<pid>\w{0,50})/$', views.getProduct, name='getProduct'),
    re_path(r'^addToCart/(?P<pid>\w{0,50})/$', views.addToCart, name='addToCart'),
    re_path(r'^Cart', views.CartView, name='Cart'),
    re_path(r'^DeleteCart', views.DeleteCart, name='DeleteCart'),
    re_path(r'^checkout', views.Checkout, name='checkout'),
    re_path(r'^orderSuccess', views.OrderSuccess, name='orderSuccess'),
    re_path(r'^orders/(?P<oid>\w{0,50})/$', views.OrderDesc, name='OrderDesc'),
    re_path(r'^editOrder/(?P<oid>\w{0,50})/$', views.getOrder, name='getOrder'),
    path('website', views.website, name='website'),
    path('project', views.project, name='project'),
    # re_path(r'^orders/update/(?P<oid>\w{0,50})/$', views.getOrder, name='getOrder'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

print('static')
print(staticfiles_urlpatterns)
print(urlpatterns)
