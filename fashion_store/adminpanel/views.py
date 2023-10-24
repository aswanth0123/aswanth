from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
from .decorator import *
from django.urls import reverse
import urllib
import json
from PIL import Image
from customers.models import *
from customers.views import outofstock

def emailpass_check(request):
    email = request.GET.get('email')
    password = request.GET.get('pass')
    check = Register.objects.filter(email=email).values_list('password')
    if check:
        email_data = ''
        encrypt_code = [i for j in check for i in j]
        verify_key = pbkdf2_sha256.verify(password, encrypt_code[0])
        if verify_key:
            password_data = ''
        else:
            password_data = 'Password Incorrect'
    else:
        email_data = f'{email} Invalid'
        password_data = ''

    context = {'email': email_data, 'pass': password_data}

    return JsonResponse(context)


@unauthencation
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        admin_details = Register.objects.filter(email=email)
        for item in admin_details:
            request.session['admin-id'] = item.id
        return redirect('/admin/dashboard/')
    else:
        already_Registed = Register.objects.all()
        return render(request, 'admin/login/login.html', {'registed': already_Registed})


def registeradmin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        check = Register.objects.all()
        if not check:
            secret_code = pbkdf2_sha256.encrypt(
                password, rounds=12000, salt_size=32)
            admin_details = Register(email=email, password=secret_code)
            admin_details.save()
            return redirect('/admin/')
        else:
            return redirect('/admin/')
    else:
        return render(request, 'admin/login/register.html')


@adminauthentication
def dashboard_admin(request):
    sales = OrderList.objects.filter(deliverystatus='Delivered').count()
    orders = OrderList.objects.filter(deliverystatus__in=['Processing','Shipped','Pending'])[:4]
    totalcustomers = register.objects.all().count()
    pendingorderscount = OrderList.objects.filter(deliverystatus__in=['Processing','Shipped','Pending']).count()
    context = {'sales':sales,'orders':orders,'customers':totalcustomers,'pending':pendingorderscount}

    return render(request, 'admin/dashboard/index.html',context)



@adminauthentication
def product_common(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['cat']
        brand = request.POST['brand']
        gender = request.POST['gender']
        details = request.POST['details']
        stylenote = request.POST.get('note')
        shipping = request.POST['shipreturn']
        check = ProductCommon.objects.filter(title=name, gender=gender, productdetail=details, stylenote=stylenote)
        if not check:
            last_productid = ProductCommon.objects.all().last()
            if last_productid:
                id2 = last_productid.productid
                value = id2[3:]
            else:
                value = 1000
            id1 = int(value)+1
            newproductid = f'FAS{id1}'
            common = ProductCommon(category=category,brand=brand,productid=newproductid, title=name, gender=gender,
                                   productdetail=details, stylenote=stylenote, shippingandreturns=shipping)
            common.save()
            message = newproductid
            return render(request, 'admin/dashboard/productcommon.html', {'id': message})
        else:
            exist = True
            return render(request, 'admin/dashboard/productcommon.html', {'exist': exist})
    else:
        return render(request, 'admin/dashboard/productcommon.html')


@adminauthentication
def product_color(request):
    totalproduct = ProductCommon.objects.all()
    if request.method == 'POST':
        # this id created by database.its used for  add foreign key of this product
        mainid = request.POST['id']
        propic = request.FILES['propic']
        pic = request.FILES['pic']
        pic2 = request.FILES['pic2']
        pic3 = request.FILES['pic3']
        color = request.POST['color']

        check = ProductColor.objects.filter(productcommon=mainid, color=color)
        if not check:
            foriegndata = ProductCommon.objects.get(id=mainid)
            colorid = f'{foriegndata.productid}/{color}'
            color_details = ProductColor(productpicture=propic, productcommon=foriegndata,
                                         colorid=colorid, picture=pic, picture2=pic2, picture3=pic3, color=color)
            color_details.save()
            context = {'products': totalproduct,
                       'colorid': colorid, 'color': color}
            return render(request, 'admin/dashboard/productcolor.html', context)
        else:
            exist = True
            context = {'products': totalproduct, 'exist': exist}
            return render(request, 'admin/dashboard/productcolor.html', context)
    else:
        context = {'products': totalproduct}
        return render(request, 'admin/dashboard/productcolor.html', context)


@adminauthentication
def product_size(request):
    totalproduct = ProductColor.objects.all()
    if request.method == 'POST':
        mainid = request.POST['id']  # this id below to productcolor table.
        size = request.POST['size']  # its used determine which product is want to add different size with price,quntity
        quty = request.POST['qunty']
        price = request.POST['price']
        check = ProductSize.objects.filter(productcolor=mainid, size=size)
        if not check:
            value = ProductColor.objects.get(id=mainid)
            sizeid = f'{value.colorid}/{size}'
            size_deatils = ProductSize(
                productcolor=value, size=size, quantity=quty, price=price, sizeid=sizeid)
            size_deatils.save()
            context = {'products': totalproduct, 'sizeid': sizeid}
            productid = value.productcommon.productid
            check_productid = ProductLists.objects.filter(productid=productid)
            if not check_productid:
                value = ProductSize.objects.filter(
                    productcolor=value, size=size, quantity=quty, price=price, sizeid=sizeid).values_list('id')
                # In this condition adding product on Productlists table.if the productid already
                sizeid = [i for j in value for i in j]
                # exist in that table its not store . so that way we can add different color and also add different size of same product
                fulldetails = ProductSize.objects.get(id=sizeid[0])
                # In home page only have one product . but inside that product have necessary colors and size
                list_details = ProductLists(
                    productfulldetails=fulldetails, productid=productid)
                list_details.save()
                return render(request, 'admin/dashboard/productsize.html', context)
            else:
                return render(request, 'admin/dashboard/productsize.html', context)
        else:
            context = {'products': totalproduct, 'exist': True}
            return render(request, 'admin/dashboard/productsize.html', context)
    else:
        context = {'products': totalproduct}
        return render(request, 'admin/dashboard/productsize.html', context)


def logout(request):
    del request.session['admin-id']
    return redirect('/')


@adminauthentication
def orders(request):
    orders = OrderList.objects.all()
    context = {'orders':orders}
    return render(request,'admin/dashboard/orders.html',context)


@adminauthentication
def customers(request):
    customers = register.objects.all()
    context = {'customers':customers}
    return render(request,'admin/dashboard/customers.html',context)


@adminauthentication
def singleorder(request):
    orderid = request.GET.get('id')
    orderdetails = OrderList.objects.filter(id=orderid)
    context = {'details':orderdetails}
    return render(request,'admin/dashboard/singleorder.html',context)



def orderaccept(request,action=None,id=None):
    OrderList.objects.filter(id=id).update(deliverystatus=action)
    url = f'/admin/singleorder/?id={id}'
    return redirect(url)

@adminauthentication
def productstatus(request):
    products = ProductLists.objects.all()
    stock = outofstock()
    context = {'products':products,'outstock':stock}
    return render(request,'admin/dashboard/status.html',context)

@adminauthentication
def productedit(request):
    productid = request.GET.get('id')
    product_details = ProductLists.objects.filter(productfulldetails__productcolor__productcommon__productid=productid)
    colorid = ProductColor.objects.filter(productcommon__productid=productid)
    print(colorid)
    context = {'product':product_details,'colorid':colorid}
    return render(request,'admin/dashboard/productedit.html',context)

@adminauthentication
def commonedit(request):
    if request.method == 'POST':
        proid = request.POST['proid']
        name = request.POST['name']
        category = request.POST['cat']
        brand = request.POST['brand']
        gender = request.POST['gender']
        details = request.POST['details']
        stylenote = request.POST.get('note')
        shipping = request.POST['shipreturn']
        url = request.POST['url']
        ProductCommon.objects.filter(productid=proid).update(title=name,category=category,brand=brand,gender=gender,productdetail=details,stylenote=stylenote,shippingandreturns=shipping)
        return redirect(url)


@adminauthentication
def sizedetails(request):
    colorid = request.GET.get('id')
    value = ProductSize.objects.filter(productcolor__id=colorid).values_list('size')
    size = [i for j in value for i in j]
    return JsonResponse({'size':size})

@adminauthentication
def sizeedit(request):
    proid = request.GET.get('id')
    size = request.GET.get('size')
    value = ProductSize.objects.filter(productcolor__id=proid,size=size).values_list('quantity','price')
    details = [i for j in value for i in j]
    info = {'qty':details[0],'price':details[1]}
    print(info)
    return JsonResponse(info)


@adminauthentication
def quantityedit(request):
    if request.method == 'POST':
        mainid = request.POST['id']
        size = request.POST['size']
        qty = request.POST['qunty']
        price = request.POST['price']
        url = request.POST['url']
        ProductSize.objects.filter(productcolor__id=mainid,size=size).update(quantity=qty,price=price)
        return redirect(url)


@adminauthentication
def productdelete(request):
    proid = request.GET.get('id')
    ProductLists.objects.filter(productfulldetails__productcolor__productcommon__productid=proid).delete()
    ProductSize.objects.filter(productcolor__productcommon__productid=proid).delete()
    ProductColor.objects.filter(productcommon__productid=proid).delete()
    ProductCommon.objects.filter(productid=proid).delete()
    return redirect('/admin/productstatus/')
