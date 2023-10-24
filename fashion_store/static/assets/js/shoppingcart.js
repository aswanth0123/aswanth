$(document).ready(function(){
    $('.tb tbody').on('change','.qty', function() {
        var currow = $(this).closest('tr')
        var price = currow.find('td:eq(1)').text()
        var last = price.slice(1)
        var quantity = currow.find('input[name="qty"]').val()
        var totalprice = parseInt(last) * parseInt(quantity)
        currow.find('td:eq(4)').html('$'+totalprice)
        subtotal()
    })

    function subtotal(){
        var total = 0
        $('table tr').each(function (){
            var value = $('td',this).eq(4).text()
            var last = parseInt(value.slice(1))
            if(!isNaN(last)){
                total += last
            }
        })
        $('#sub').html('$'+total)
        $('#side-price').html('$'+total)
        $('#side-price2').html('$'+total)
        $('#sub2').html('$'+total)
    }
    $('.shipping-charge').on('change',function(){
        var charge = $('input[name="shipping"]:checked').val();
        var total = $('#sub').text()
            total = total.slice(1)
        var subtotal = parseInt(charge)+parseInt(total)
        $('#sub2').html('$'+subtotal)
    })
})
