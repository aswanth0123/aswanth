from django.urls import path
from .models import *
from customers import views

urlpatterns = [
    path('',views.home),
    path('register/',views.user_register),
    path('emailpasswordcheck/',views.emailpassword),
    path('emailpasswordchecklogin/',views.emailpasswordlogin),
    path('login/',views.user_login),
    path('productsingle/',views.product_single),
    path('addtocart/',views.addtocart),
    path('sidecart/',views.sidecart),
    path('shoppingcart/',views.shoppingcart),
    path('logincheck/',views.logincheck),
    path('logout/',views.userlogout),
    path('account/',views.customer_account),
    path('checkout/',views.checkout),
    path('deleteproduct/',views.deleteproduct),
    path('personaldetails/',views.personaldetails),
    path('passwordchange/',views.passwordchange),
    path('address/',views.address),
    path('oldpassconfirm/',views.oldpassconfirm),
    path('category/',views.category),
    path('filter/<cat>/<gen>/<siz>/<bra>/<pri>/',views.filter),
    path('productreview/',views.productreview),
    path('search/',views.search),
    path('subcription/',views.subcription),
    \


]
