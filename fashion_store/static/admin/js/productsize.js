$(document).ready(function(){
    $('#proid').change(function(){
        var productid = $(this).val()
        $.ajax({
            url:'/admin/sizedetails/',
            data:{'id':productid},
            success: function(response){
                $('#prosize').empty()
                $('#prosize').html(`<option value=''>Select</option>`)
                for (var i=0; i<response.size.length; i++){
                    $('#prosize').append(`<option value="${response.size[i]}">${response.size[i]}</option>`)
                }
            }
        })
    })
    $('#prosize').on('change',function (){
        var productid = $('#proid').val()
        var size = $(this).val()
        $.ajax({
            url:'/admin/sizeedit/',
            data:{'id':productid,'size':size},
            success: function(response){
                $('#qty').val(response.qty)
                $('#price').val(response.price)
            }
        })
    })
})
