
from django.urls import path
from . import views
urlpatterns = [
    path('',views.login),
    path('logout/',views.logout),
    path('register/',views.registeradmin),
    path('emailpasscheck/',views.emailpass_check),
    path('dashboard/',views.dashboard_admin),
    path('common/',views.product_common),
    path('color/',views.product_color),
    path('size/',views.product_size),
    path('orders/',views.orders),
    path('customers/',views.customers),
    path('singleorder/',views.singleorder),
    path('orderaccept/<action>/<id>/',views.orderaccept),
    path('productstatus/',views.productstatus),
    path('productedit/',views.productedit),
    path('commonedit/',views.commonedit),
    path('sizedetails/',views.sizedetails),
    path('sizeedit/',views.sizeedit),
    path('quantityedit/',views.quantityedit),
    path('productdelete/',views.productdelete),

    # path('photocheck/',views.photo_check),
]
