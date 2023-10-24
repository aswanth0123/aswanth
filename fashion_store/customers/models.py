from django.db import models
from adminpanel.models import *
from django.utils import timezone

class register(models.Model):
    name = models.CharField(max_length=200,default='')
    email = models.CharField(max_length=200,default='')
    phoneno = models.CharField(max_length=20,default='')
    password = models.CharField(max_length=200,default='')
    fname = models.CharField(max_length=200,default='')
    lname = models.CharField(max_length=200,default='')
    gender = models.CharField(max_length=200,default='')


class CartList(models.Model):
    productid = models.ForeignKey(ProductSize,on_delete=models.CASCADE)
    session = models.CharField(max_length=500,default='')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)


class OrderList(models.Model):
    orderid = models.CharField(max_length=200,default='')
    customerid = models.ForeignKey(register,on_delete=models.CASCADE)
    productid = models.ForeignKey(ProductSize,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    shippingcharge = models.IntegerField(default=0)
    totalprice = models.CharField(max_length=200,default='')
    address = models.CharField(max_length=5000,default='')
    bookeddate = models.DateField(default=timezone.now)
    deliverydate = models.DateTimeField(default='')
    payment = models.CharField(max_length=200,default='')
    deliverystatus = models.CharField(max_length=200,default='')

class CustomerAddress(models.Model):
    customerid = models.ForeignKey(register,on_delete=models.CASCADE)
    house = models.CharField(max_length=2000,default='')
    nearlocation = models.CharField(max_length=2000,default='')
    city = models.CharField(max_length=2000,default='')
    state = models.CharField(max_length=200,default='')
    pincode = models.CharField(max_length=200,default='')
    phone = models.CharField(max_length=200,default='')

class CheckoutToken(models.Model):
    customerid = models.CharField(max_length=200,default='')
    tokenno = models.CharField(max_length=200,default='')


class ProductReview(models.Model):
    customerid = models.ForeignKey(register,on_delete=models.CASCADE)
    colorid = models.ForeignKey(ProductColor,on_delete=models.CASCADE)
    starpercent = models.IntegerField(default=0)
    createdtime = models.DateTimeField(default=timezone.now)
    like = models.IntegerField(default=0)
    delike = models.IntegerField(default=0)
    review = models.CharField(max_length=4000,default='')

class ProductReviewLikes(models.Model):
    productreview = models.ForeignKey(ProductReview,on_delete=models.CASCADE)
    customerid = models.ForeignKey(register,on_delete=models.CASCADE)
    likestatus = models.CharField(max_length=50,default='')

class Subcription(models.Model):
    email = models.EmailField(max_length=200,default='')
