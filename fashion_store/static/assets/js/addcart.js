function addcart() {
    var sizeid = $('#size').val()
    if (sizeid > 0){
        $.ajax({
            url: '/addtocart/',
            data: { 'id': sizeid },
            success: function (data) {
                if (data.status == 'item added') {
                    $('#cartclick').html('Go to Cart')
                    sidecart()
                } else {
                    alert(data.status)
                }

            }
        });
    }else{
        alert('Please select a size')
    }

}

function sidecart() {
    $.ajax({
        url: '/sidecart/',
        dataType: 'json',
        success: function (data) {
            var idlist = []
            $('.cart').each(function () {
                idlist.push(this.id)
            })
            if (data.lists.length > 1) {

                for (var i = 0; i < data.lists.length; i++) {
                    if (idlist.includes(data.lists[i].id)) {
                        continue
                    }
                    else {
                        lastid = idlist[idlist.length - 1]
                        $(`<div class="product"><div class="product-cart-details"><h4 class="product-title"><a href="/productsingle/?id2=${data.lists[i].productid}">${data.lists[i].name}</a></h4><span class="cart-product-info"><span class="cart-product-qty"></span>${data.lists[i].size}</span><br><span class="cart-product-info"><span class="cart-product-qty"></span>$${data.lists[i].price}</span></div><figure class="product-image-container"><a href="/productsingle/?id2=${data.lists[i].productid}" class="product-image"><img src="${data.lists[i].link}" alt="product"></a></figure></div>`).insertAfter(`#${lastid}`)
                    }
                }
                $('#count').html(data.count)
                $('#price').html('$' + data.price)
                $('#price2').html('$' + data.price)
            } else {
                for (var j = 0; j < data.lists.length; j++) {
                    $('.cart').html(`<div class="product"><div class="product-cart-details"><h4 class="product-title"><a href="/productsingle/?id2=${data.lists[j].productid}">${data.lists[j].name}</a></h4><span class="cart-product-info"><span class="cart-product-qty"></span>${data.lists[j].size}</span><br><span class="cart-product-info"><span class="cart-product-qty"></span>$${data.lists[j].price}</span></div><figure class="product-image-container"><a href="/productsingle/?id2=${data.lists[j].productid}" class="product-image"><img src="${data.lists[j].link}" alt="product"></a></figure></div>`)
                    $('#count').html(data.count)
                    $('#price').html('$' + data.price)
                    $('#price2').html('$' + data.price)
                }
                location.reload()
            }
        }
    })
}
