from django.shortcuts import render,redirect
from customers.models import *
from adminpanel.models import *

def customerauthentication(data_fun):
    def check(request):
        if request.session.has_key('customer-id'):
            return data_fun(request)
        else:
            return redirect('/')
    return check

def sessioncreation(data_fun):
    def check(request):
        if request.session.has_key('customer-id'):
            customerid = 'custo-'+str(request.session['customer-id'])
            current_sessionid = request.session['guest-session']
            value = CartList.objects.filter(session=current_sessionid).values_list('productid__id')
            idlist = [i for j in value for i in j]
            if idlist:
                for item in idlist:
                    product_exist = CartList.objects.filter(session=customerid,productid__id=item)
                    if not product_exist:
                        product_details = ProductSize.objects.get(id=item)
                        value2 = CartList.objects.filter(productid__id=item).values_list('quantity','price')
                        prqty = [i for j in value2 for i in j]
                        CartList.objects.create(session=customerid,productid=product_details,quantity=prqty[0],price=prqty[1])

            request.session['customer-session'] = customerid
            return data_fun(request)
        else:
            if request.session.has_key('guest-session'):
                return data_fun(request)
            else:
                lastguest = CartList.objects.all().last()
                if lastguest:
                    lastguestid = lastguest.session
                    questid = f'guest-{int(lastguestid[6:])+1}'
                else:
                    questid = 'guest-1'
                request.session['guest-session'] = questid
                return data_fun(request)
    return check


def checkoutauthentication(function):
    def check(request):
        if request.session.has_key('customer-id'):
            sessionid = request.session['customer-session']
            cart_item = CartList.objects.filter(session=sessionid)
            if cart_item:
                value = CartList.objects.filter(session=sessionid).values_list('id')
                cartids = [i for j in value for i in j]
                price = 0
                for item in cartids:
                    pro_details = CartList.objects.get(id=item)
                    price += int(pro_details.productid.price)*(pro_details.quantity)
                value = CartList.objects.filter(session=sessionid).values_list('quantity')
                qty = [i+i for j in value for i in j]
                count = 0
                for item in qty:
                    count += item           #here creating token for unautherized access.
                tokenno = count+price       #token will delete after order placed

                check = CheckoutToken.objects.filter(customerid=sessionid,tokenno=tokenno)
                if check:
                    return function(request)
                else:
                    return redirect('/shoppingcart/')
            else:
                return redirect('/')

        else:
            return redirect('/shoppingcart/')
    return check
