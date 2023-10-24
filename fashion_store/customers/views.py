from django.shortcuts import render,HttpResponse
from .models import *
import requests
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
from .decorator import *
from adminpanel.models import *
from django.core.serializers import serialize
import json
import random
import datetime
from django.db.models import Q


def outofstock():
    value = ProductSize.objects.filter(quantity__lte=0).values_list(
        'productcolor__productcommon__productid')
    if value:

        totalid = [i for j in value for i in j]

        out_of_stock = []
        for id in totalid:
            if id not in out_of_stock:
                count = totalid.count(id)
                totalsize = ProductSize.objects.filter(
                    productcolor__productcommon__productid=id).count()
                if count == totalsize:
                    out_of_stock.append(id)
                else:
                    pass
        return out_of_stock
    else:
        out_of_stock = []
        return out_of_stock


def ratecalculator():
    value = ProductCommon.objects.all().values_list('productid')
    productids = [i for j in value for i in j]

    for item in productids:
        value2 = ProductReview.objects.filter(colorid__productcommon__productid=item).values_list('starpercent')
        rates = [i for j in value2 for i in j]
        if rates:
            totalrate = 0
            for i in rates:
                totalrate += i

            lastrate = totalrate / len(rates)
            ProductCommon.objects.filter(productid=item).update(ratepercentage=lastrate,ratecount=len(rates))
        else:
            pass


def customerlogincheck(request):
    if request.session.has_key('customer-id'):
        return True
    return False

@sessioncreation
def home(request):
    customer = customerlogincheck(request)
    sessionid = request.session['customer-session'] if customer else request.session['guest-session']
    allcloths = ProductLists.objects.all()
    productcolor = ProductColor.objects.all()
    cartlist = CartList.objects.filter(session=sessionid)
    productcount = CartList.objects.filter(session=sessionid).count()
    totalprice = price(sessionid)
    stock = outofstock()
    ratecalculator()
    value = ProductSize.objects.all().values_list('productcolor')
    colorsize = [i for j in value for i in j]
    context = {'customerexist':customer,'procount': productcount, 'totalprice': totalprice, 'cloths': allcloths,
               'stock': stock, 'color': productcolor, 'colorsize': colorsize, 'cart': cartlist}
    return render(request, 'customer/homepage/index.html', context)


def emailpasswordlogin(request):
    emailid = request.GET.get('email')
    password = request.GET.get('password')
    email_details = register.objects.filter(email=emailid)
    if password:
        password_deatils = register.objects.filter(
            email=emailid).values_list('password')
    else:
        password_deatils = ''

    if email_details:
        email_data = False
    else:
        email_data = f'{emailid} email Invalid' if emailid else ''

    if password_deatils:
        encrypted = [i for j in password_deatils for i in j]
        verify = pbkdf2_sha256.verify(password, encrypted[0])

        value = False if verify else ' Password Incorrect '
    else:
        value = False

    info = {'email': email_data, 'password': value}
    return JsonResponse(info)


def emailpassword(request):
    emailid = request.GET.get('email')
    phone = request.GET.get('phone')
    email_details = register.objects.filter(email=emailid)
    phone_details = register.objects.filter(phoneno=phone)

    email_data = "Email Already exist" if email_details else False

    phone_data = 'Phone Number already exist' if phone_details else False

    info = {'phoneno': phone_data, 'emailid': email_data}
    return JsonResponse(info)

def user_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['pass']
        url = request.POST['url']
        hashpassword = pbkdf2_sha256.encrypt(
            password, rounds=12000, salt_size=32)
        check = register.objects.filter(email=email)
        if not check:
            # message = f'Welcome to Fashionstore'
            # send_sms(phone, message)
            register.objects.create(
                email=email,name=name, phoneno=phone, password=hashpassword)
            return redirect(url)
        else:
            return redirect(url)
    else:
        return render(request, 'customer/homepage/index.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['emailid']
        password = request.POST['password']
        url = request.POST['url']
        customer = register.objects.filter(email=email)
        if customer:
            for item in customer:
                request.session['customer-id'] = item.id
                check2 = CustomerAddress.objects.filter(customerid__id=item.id)
                if not check2:
                    details = register.objects.get(id=item.id)
                    CustomerAddress.objects.create(customerid=details)
                break
            return redirect(url)
        else:
            return render(request, 'customer/homepage/index.html')
    else:
        return render(request, 'customer/homepage/index.html')

def userlogout(request):
    del request.session['customer-id']
    return redirect('/')


@sessioncreation
def product_single(request):
    customer = customerlogincheck(request)
    sessionid = request.session['customer-session'] if customer else request.session['guest-session']
    colorid = request.GET.get('id2')
    ratecalculator()
    totalcolors = ProductColor.objects.all()
    totalsize = ProductSize.objects.filter(quantity__gte=1).order_by('-size')
    value = ProductSize.objects.all().values_list('productcolor')
    colorsize = [i for j in value for i in j]

    customerid = request.session['customer-id'] if customer else 0

    latest_item = ProductSize.objects.filter(
        productcolor__colorid=colorid).latest()
    totalreviewcount = ProductReview.objects.filter(colorid=latest_item.productcolor.id).count()
    totalreview = ProductReview.objects.filter(colorid=latest_item.productcolor.id)
    review = ProductReview.objects.filter(customerid=customerid,colorid=latest_item.productcolor.id)
    product_details = ProductSize.objects.filter(id=latest_item.id)

    value2 = ProductSize.objects.filter(productcolor__colorid=colorid).values_list('productcolor__productcommon__category','productcolor__productcommon__gender')
    category = [i for j in value2 for i in j ]
    productcategory = ProductLists.objects.filter(productfulldetails__productcolor__productcommon__category=category[0],productfulldetails__productcolor__productcommon__gender=category[1]).order_by('-productfulldetails__productcolor__productcommon__createddate')
    stock = outofstock()

    cartlist = CartList.objects.filter(session=sessionid)
    productcount = CartList.objects.filter(session=sessionid).count()
    totalprice = price(sessionid)

    context = {'stock':stock,'otherproduct':productcategory,'totalreviewcount':totalreviewcount,'totalreview':totalreview,'review':review,'customerexist':customer,'totalprice': totalprice, 'procount': productcount, 'cart': cartlist,
               'pro_Details': product_details, 'size': totalsize, 'color': totalcolors, 'colorsize': colorsize}
    return render(request, 'customer/homepage/productsingle.html', context)


@sessioncreation
def addtocart(request):
    customer = customerlogincheck(request)
    sessionid = request.session['customer-session'] if customer else request.session['guest-session']
    sizeid = request.GET.get('id')
    checkproduct = CartList.objects.filter(productid=sizeid, session=sessionid)
    if checkproduct:
        return JsonResponse({'status': 'Product already in cart'})
    else:
        size_details = ProductSize.objects.get(id=sizeid)
        CartList.objects.create(productid=size_details, session=sessionid)
        return JsonResponse({'status': 'item added'})


def price(id):
    value = CartList.objects.filter(session=id).values_list('id')
    cartids = [i for j in value for i in j]
    price = 0
    for item in cartids:
        pro_details = CartList.objects.get(id=item)
        price += int(pro_details.productid.price)*(pro_details.quantity)

    return price


@sessioncreation
def sidecart(request):
    customer = customerlogincheck(request)
    sessionid = request.session['customer-session'] if customer else request.session['guest-session']
    if sessionid:
        cartlists = CartList.objects.filter(session=sessionid)
        if cartlists:
            productcount = CartList.objects.filter(session=sessionid).count()
            totalprice = price(sessionid)
            value = CartList.objects.filter(
                session=sessionid).values_list('productid')
            idlist = [i for j in value for i in j]
            totallists = []

            for item in idlist:
                productdetails = ProductSize.objects.get(id=item)
                productlist = {}
                productlist['id'] = str(productdetails.id)
                productlist['name'] = productdetails.productcolor.productcommon.title
                productlist['link'] = productdetails.productcolor.picture.url
                productlist['price'] = productdetails.price
                productlist['productid'] = productdetails.productcolor.colorid
                productlist['size'] = productdetails.size
                totallists.append(productlist)
            info = {'lists': totallists,
                    'count': productcount, 'price': totalprice}
            return JsonResponse(info)
        else:
            return JsonResponse({'info': 'Cart Empty'})
    else:
        return JsonResponse({'info': 'Cart Empty'})

@sessioncreation
def shoppingcart(request):
    customer = customerlogincheck(request)
    sessionid = request.session['customer-session'] if customer else request.session['guest-session']
    cartlist = CartList.objects.filter(session=sessionid)
    productcount = CartList.objects.filter(session=sessionid).count()
    totalprice = price(sessionid)
    context = {'cart':cartlist,'customerexist':customer,'procount': productcount, 'totalprice': totalprice,}
    return render(request,'customer/homepage/shoppingcart.html',context)


@sessioncreation
def logincheck(request):
    value = json.loads(request.GET.get('dic'))
    for i in value:
        CartList.objects.filter(id=i['id']).update(quantity=i['qty'],price=i['price'])

    if request.session.has_key('customer-id'):
        customerid = request.session['customer-id']
        sessionid = request.session['customer-session']
        total = price(sessionid)
        value2 = CartList.objects.filter(session=sessionid).values_list('quantity')
        qty = [i+i for j in value2 for i in j]
        count = 0
        for item in qty:
            count += item           #here creating token for unautherized access.
        tokenno = count+total       #token will delete after order placed

        check = CheckoutToken.objects.filter(customerid=sessionid,tokenno=tokenno)
        if not check:
            CheckoutToken.objects.create(customerid=sessionid,tokenno=tokenno)



        status = True
    else:
        status = False
    return JsonResponse({'status':status})


@customerauthentication
def customer_account(request):
    customer = customerlogincheck(request)
    customerid = request.session['customer-id']
    sessionid = request.session['customer-session'] if customer else request.session['guest-session']
    cartlist = CartList.objects.filter(session=sessionid)
    productcount = CartList.objects.filter(session=sessionid).count()
    totalprice = price(sessionid)
    orders = OrderList.objects.filter(customerid=customerid)
    account = register.objects.filter(id=customerid)
    address = CustomerAddress.objects.filter(customerid=customerid)
    context = {'address':address,'account':account,'orders':orders,'customerexist':customer,'cart':cartlist,'customerexist':customer,'procount': productcount, 'totalprice': totalprice}
    return render(request,'customer/homepage/account.html',context)


def generate_order_id(price,customerid):
    generate = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 7)])
    orderid = f'OD{price}{customerid}{generate}'
    return orderid


def quantityminus(productid,qty):
    product = ProductSize.objects.get(id=productid)
    newquantity = product.quantity - qty
    ProductSize.objects.filter(id=productid).update(quantity=newquantity)



@checkoutauthentication
def checkout(request):
    sessionid = request.session['customer-session']
    sessionid2 = request.session['guest-session']
    customerid = request.session['customer-id']
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        house = request.POST['house']
        nearlocation = request.POST['nearl']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        phone = request.POST['phone']
        email = request.POST['email']
        totalprice = price(sessionid)
        CustomerAddress.objects.filter(customerid__id=customerid).update(phone=phone,house=house,nearlocation=nearlocation,city=city,state=state,pincode=pincode)
        register.objects.filter(id=customerid).update(fname=fname,lname=lname)

        address = "{0} {1},\n{2} {3},{4}\n{5}\n{6}".format(fname,lname,house,city,state,nearlocation,phone)
        customer_details = register.objects.get(id=customerid)
        value = CartList.objects.filter(session=sessionid).values_list('id')
        total_cart_items = [i for j in value for i in j]
        for item in total_cart_items:
            product = CartList.objects.get(id=item)
            productdetails = ProductSize.objects.get(id=product.productid.id)
            orderid = generate_order_id(totalprice,item)
            qty = product.quantity
            totalprice = product.price
            shippingcharge = 0
            todaydate = datetime.datetime.now()
            deliverydate = (todaydate + datetime.timedelta(days=7)).date()
            payment = 'COD'
            check = OrderList.objects.filter(orderid=orderid,customerid=customer_details,productid=productdetails,quantity=qty,shippingcharge=shippingcharge,totalprice=totalprice,address=address,bookeddate=todaydate,deliverydate=deliverydate,payment=payment)
            if not check:
                OrderList.objects.create(orderid=orderid,customerid=customer_details,productid=productdetails,quantity=qty,shippingcharge=shippingcharge,totalprice=totalprice,address=address,bookeddate=todaydate,deliverydate=deliverydate,payment=payment,deliverystatus='Pending')
                productid = product.productid.id
                quantityminus(productid,qty)
                CartList.objects.filter(id=item).delete()
                CartList.objects.filter(session=sessionid2).delete()

        CheckoutToken.objects.filter(customerid=sessionid).delete()
        return redirect('/account/')
    else:
        customer = customerlogincheck(request)
        cartlist = CartList.objects.filter(session=sessionid)
        productcount = CartList.objects.filter(session=sessionid).count()
        totalprice = price(sessionid)
        address = CustomerAddress.objects.filter(customerid__id=customerid)
        context = {'address':address,'cart':cartlist,'customerexist':customer,'procount': productcount, 'totalprice': totalprice}
        return render(request,'customer/homepage/checkout.html',context)


def deleteproduct(request):
    productid = request.GET.get('id')
    CartList.objects.filter(id=productid).delete()
    return redirect('/shoppingcart/')

@customerauthentication
def personaldetails(request):
    customerid = request.session['customer-id']
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        register.objects.filter(id=customerid).update(fname=fname,lname=lname,email=email,phoneno=phone,gender=gender)
        return redirect('/account/')


@customerauthentication
def passwordchange(request):
    customerid = request.session['customer-id']
    if request.method == 'POST':
        newpassword = request.POST['new']
        secret_code = pbkdf2_sha256.encrypt(
            newpassword, rounds=12000, salt_size=32)
        register.objects.filter(id=customerid).update(password=secret_code)
        return redirect('/account/')

@customerauthentication
def address(request):
    customerid = request.session['customer-id']
    if request.method == 'POST':
        house = request.POST['house']
        nearlocation = request.POST['nearl']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        phone = request.POST['phone']
        CustomerAddress.objects.filter(customerid=customerid).update(house=house,nearlocation=nearlocation,city=city,state=state,pincode=pincode,phone=phone)
        return redirect('/account/')

def oldpassconfirm(request):
    customerid = request.session['customer-id']
    oldpass = request.GET.get('pass')
    details = register.objects.get(id=customerid)
    verify = pbkdf2_sha256.verify(oldpass,details.password)
    status = False if verify else 'Old Password Incorrected'
    return JsonResponse({'info':status})

@sessioncreation
def category(request):
    customer = customerlogincheck(request)
    sessionid = request.session['customer-session'] if customer else request.session['guest-session']
    cartlist = CartList.objects.filter(session=sessionid)
    productcount = CartList.objects.filter(session=sessionid).count()
    totalprice = price(sessionid)
    products = ProductLists.objects.all()
    stock = outofstock()
    ratecalculator()
    kurtas = ProductCommon.objects.filter(category='Kurtas').count()
    tshirts = ProductCommon.objects.filter(category='T-shirts').count()
    shirts = ProductCommon.objects.filter(category='Shirts').count()
    jacket = ProductCommon.objects.filter(category='Jackets').count()
    jeans = ProductCommon.objects.filter(category='jeans').count()
    print(products)
    productcolor = ProductColor.objects.all()
    value = ProductSize.objects.all().values_list('productcolor')
    colorsize = [i for j in value for i in j]
    context = {'jeans':jeans,'jacket':jacket,'shirts':shirts,'tshirts':tshirts,'kurtas':kurtas,'color':productcolor,'colorsize':colorsize,'stock':stock,'products':products,'customerexist':customer,'procount': productcount, 'totalprice': totalprice,'cart':cartlist}
    return render(request,'customer/homepage/category.html',context)


def filter(request):

    context = {'jeans':jeans,'jacket':jacket,'shirts':shirts,'tshirts':tshirts,'kurtas':kurtas,'color':productcolor,'colorsize':colorsize,'stock':stock,'products':query,'customerexist':customer,'procount': productcount, 'totalprice': totalprice,'cart':cartlist}
    return render(request,'customer/homepage/category.html',context)


@customerauthentication
def productreview(request):
    customerid = request.session['customer-id']
    ratecalculator()
    if request.method == "POST":
        customer_details = register.objects.get(id=customerid)
        colorid = request.POST['proid']
        review = request.POST['review']
        star = int(request.POST['star'])
        url = request.POST['url']
        product = ProductColor.objects.get(id=colorid)
        check = ProductReview.objects.filter(customerid=customer_details,colorid=product)
        if not check:
            ProductReview.objects.create(review=review,starpercent=star,customerid=customer_details,colorid=product)
            return redirect(url)
        else:
            reviewid = request.POST['reviewid']
            ProductReview.objects.filter(id=reviewid).update(review=review,starpercent=star)
            return redirect(url)

@sessioncreation
def search(request):
    query = request.GET.get('q')
    url = f'/filter/{query}&/all/all/all/0,750/'
    return redirect(url)


def subcription(request):
    email = request.POST['email']
    check = Subcription.objects.filter(email=email)
    if not check:
        Subcription.objects.create(email=email)

    return redirect('/')
