from django.shortcuts import render, redirect
# from MyApp.models import User
from MyApp.forms import FormNewUser,FormUserProfileInfo,FormLogin,FormAddProduct,FormEditProfile,FormEditOrder
#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from MyApp.models import UserProfileInfo,Product, Cart, Order
from django.contrib.auth.models import User

from django.views.generic import ListView
import razorpay
import json

def website(request):
    return render(request, 'Bobby/home.html')

class ProductList(ListView):
    model = Product

# Create your views here.
def index(request):
#     userList = UserProfileInfo.objects.all()
#     for user in userList:
#         print(user.profile_pic)
#     userDict = {'users': userList}
    return render(request, 'index.html')

@login_required
def add_product(request):
    form = FormAddProduct()
    if request.method == "POST":
        product_form = FormAddProduct(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            product.product_available = True
            product.save()

            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']

            product.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(product_form.errors)

    else:
        product_form = FormAddProduct()
                                        # 'form': form
    return render(request, 'addProduct.html', {'product_form':product_form})

@login_required
def edit_product(request,pid):
    product = Product.objects.get(id=pid)
    if request.method == "POST":
        product_form = FormAddProduct(request.POST,instance = product)   ## add instance
        if product_form.is_valid():
            product = product_form.save()
            product.save()

            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']

            product.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(product_form.errors)

    else:
        product_form = FormAddProduct()   ## add instance

    return render(request, 'addProduct.html', {'product_form':product_form})  # 'form': form



def signup(request):
    form = FormNewUser()
    if request.method == "POST":
        user_form = FormNewUser(request.POST)
        profile_form = FormUserProfileInfo(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = FormNewUser()
        profile_form = FormUserProfileInfo()
                                        # 'form': form
    return render(request, 'users.html', {'user_form':user_form,'profile_form':profile_form})

def user_login(request):
    form = FormLogin()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user = user)
                # return HttpResponse("Account Active")
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Login Failed")
            print("Username:{} Password:{}".format(username,password))
            return render(request,'login.html',{"failed": True})

    else:
        return render(request,'login.html',{})

# form = FormLogin(request.POST)
# if form.is_valid():
#     return index(request)
# else:
#     print("ERROR FORM INVALID")

# return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    # return HttpResponse("Logged Out")
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_profile(request):
    username = request.user.username
    print(username)
    userid = request.user.UserProfileInfo.somaiya_id
    print(userid)
    return render(request, 'userProfile.html', {})

@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = FormEditProfile(request.POST, instance=request.user)
        profile_form = FormUserProfileInfo(request.POST, instance = request.user.UserProfileInfo)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = FormEditProfile(instance=request.user)
        profile_form = FormUserProfileInfo(instance=request.user.UserProfileInfo)
                                        # 'form': form
    return render(request, 'editUserProfile.html', {'user_form':user_form,'profile_form':profile_form})

@login_required
def menuPage(request):
    productList = Product.objects.all()
    productDict = {'products':productList}
    return render(request, 'canteenMenu.html', productDict)


def getProduct(request, pid):
    # print(pid)
    product = Product.objects.get(id=pid)
    order = Order(user = request.user, product = product, order_state = False)
    order.save()
    # productDict = {'product':productList}
    # return render(request, 'canteenMenu.html', {"product":product})
    return redirect(product.product_buyLink)



def addToCart(request,pid):
    print(pid)
    product = Product.objects.get(id=pid)
    currUser = request.user
    try:
        existingCart = Cart.objects.get(item=product, user=currUser, order_id=0)
        existingCart.quantity += 1
        existingCart.total = product.product_cost * existingCart.quantity
        existingCart.save()
        print(existingCart)
    except:
        quantity = 1
        total = product.product_cost * quantity
        # thisCart = Cart.objects.create(user=currUser, item=Product, quantity=quantity, total=total)
        thisCart = Cart(user=currUser, item=product, quantity=quantity, total=total)
        thisCart.save()
    productList = Product.objects.all()
    productDict = {'products':productList}
    return render(request, 'canteenMenu.html', productDict)

def CartView(request):
    existingCart = Cart.objects.filter(order_id=0)

    if existingCart:
        totalBill = 0
        for item in  existingCart:
            totalBill += item.total
        cartData = {'exists': True, 'existingCart': existingCart, 'totalBill': totalBill}
        print(cartData)
        return render(request, 'Cart.html', cartData)
    else:
        cartData = {'exists': False}
        print(cartData)
        return render(request, 'Cart.html', cartData)

def DeleteCart(request):
    print('Deleting Cart')
    Cart.objects.filter(order_id=0).delete()
    productList = Product.objects.all()
    productDict = {'products':productList}
    return render(request, 'canteenMenu.html', productDict)

def Checkout(request):
    existingCart = Cart.objects.filter(order_id=0)
    currUser = request.user
    razorpay_order_id = "0"
    razorpay_payment_id = "0"
    razorpay_signature = "0"
    thisOrder = Order(user=currUser, razorpay_payment_id=razorpay_payment_id, razorpay_order_id=razorpay_order_id, razorpay_signature=razorpay_signature)
    thisOrder.save()
    newOrderId = thisOrder.id
    orderTotal = 0
    OrderCart = Cart.objects.filter(order_id=0)
    temp = True
    desc = ''
    for item in OrderCart:
        if temp:
            pImgUrl = "http://127.0.0.1:8000" + item.item.product_image.url
            temp = False
        desc += item.item.product_name + " x " + str(item. quantity) + ", "
        orderTotal += item.total
        item.order_id = newOrderId
        item.save()
    thisOrder.orderTotal = orderTotal
    thisOrder.save()
    order_amount = orderTotal*100
    order_currency = 'INR'
    order_receipt = 'order_rcptid_' + str(thisOrder.id)
    client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY", "YOUR_RAZORPAY_SECRET"))
    notes = {'Shipping address': 'Bommanahalli, Bangalore'}
    orderDict = {'amount': order_amount, "currency" : order_currency, "receipt" : order_receipt, "notes": notes, "payment_capture": "1"}
    orderResp = client.order.create(orderDict)
    thisOrder.razorpay_order_id = orderResp.get('id')
    thisOrder.paymentStatus = "Failed"
    thisOrder.save()
    PaymentData = {}
    PaymentData['order_id'] = orderResp.get('id')
    PaymentData['pImgUrl'] = pImgUrl
    PaymentData['total_amount'] = order_amount
    PaymentData['username'] = currUser.username
    PaymentData['useremail'] = currUser.email
    PaymentData['desc'] = desc
    print("Payment Data: ", PaymentData)
    newExistingCart = Cart.objects.filter(order_id=thisOrder.id)
    print("newExistingCart: ", newExistingCart)
    return render(request, 'checkout.html', {"existingCart": newExistingCart, 'PaymentData':PaymentData, "totalBill":orderTotal })

def OrderSuccess(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        razorData = {'razorpay_payment_id':razorpay_payment_id, 'razorpay_order_id':razorpay_order_id, 'razorpay_signature':razorpay_signature}
        client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY", "YOUR_RAZORPAY_SECRET"))
        client.utility.verify_payment_signature(razorData)
        currOrder = Order.objects.get(razorpay_order_id=razorpay_order_id)
        currOrder.razorpay_payment_id = razorpay_payment_id
        currOrder.razorpay_signature = razorpay_signature
        currOrder.paymentStatus = "Paid Successfully"
        currOrder.save()
    return render(request, 'paymentSuccess.html')

def ViewOrders(request):
    currUser = request.user
    if currUser.is_staff:
        allOrders = Order.objects.all()
        return render(request, 'orders.html', {"allOrders": allOrders})
    else:
        allOrders = Order.objects.filter(user=currUser)
        return render(request, 'orders.html', {"allOrders": allOrders})

def OrderDesc(request, oid):
    existingCart = Cart.objects.filter(order_id=oid)
    currOrder = Order.objects.get(id=oid)
    return render(request, 'orderDesc.html', {"existingCart": existingCart, 'order':currOrder})

@login_required
def getOrder(request,oid):
    order = Order.objects.get(id=oid)
    if request.method == "POST":
        order_form = FormEditOrder(request.POST,instance = order)   ## add instance
        if order_form.is_valid():
            print(order_form)
            order = order_form.save()
            print(order)
            order.save()
            return HttpResponseRedirect(reverse('ViewOrders'))
        else:
            print(order_form.errors)
    else:
        order_form = FormEditOrder()   ## add instance
    return render(request, 'editOrder.html', {'order_form':order_form, 'order':order})  # 'form': form

# def OrderState(request,oid):
#     order = Order.objects.get(id=oid)
#         if request.method == "POST":
#             if
#     return render(request, 'orderState.html', {'order':order})
