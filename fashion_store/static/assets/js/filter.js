$(document).ready(function(){
    $('#apply').on('click',function(){
        var category = ''
        var gender = ''
        var size = ''
        var brand = ''
        var price = $('#price-slider').text()
            price = price.split('$')

        category = $('input[name=category]:checked').val()+'&'

        gender = $('input[name=gender]:checked').val()+'&'

        $('input:checkbox[name=size]:checked').each(function(){
            size += `${$(this).val()}&`
        })

        $('input:checkbox[name=brand]:checked').each(function(){
            brand += `${$(this).val()}&`
        })



        url = "/filter/"

        if(category == 'undefined&'){
            url += 'all/'
        }else{
            url += category+'/'
        }

        if(gender == 'undefined&'){
            url += 'all/'
        }else{
            url += gender+'/'
        }

        if(size != ''){
            url += size+'/'
        }else{
            url += 'all/'
        }

        if(brand != ''){
            url += brand+'/'
        }else{
            url += 'all/'
        }

        if(price != ''){
            url += price
        }else{
            url += 'all'
        }

        $(location).attr('href', url)
    })

    $('#clear').click(function (){
        $('.sidebar-shop').find('input').prop('checked', false);
    })
})
