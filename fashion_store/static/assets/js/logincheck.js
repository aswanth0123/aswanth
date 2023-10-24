$(document).ready(function (){
    $('#submit').on('click',function(){
        var result = []
        $('table tr').each(function (){
            var id = parseInt(this.id)
            var qty = parseInt($('.qty',this).val())
            var price = $('#price',this).text()
                price = parseInt(price.slice(1))
            if(!isNaN(id)){
                result.push({'id':id,'qty':qty,'price':price})
            }
        })
        var value = JSON.stringify(result)
        console.log(value)
        $.ajax({
            url:'/logincheck/',
            data:{'dic':value},
            success:function(item){
                window.stop()
                if (item.status == false){
                    window.stop()
                    $('#login').click()

                }else if(item.status == true){
                    $(location).attr('href', '/checkout/')
                }
            }

        })
    })
})
