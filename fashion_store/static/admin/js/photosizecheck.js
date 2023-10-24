$(document).ready(function () {
    $('#propic').change(function (){
        var fd = new FormData()
        var image = $('#propic')[0].files[0]
        fd.append('image',image)
        $.ajax({
            type: 'POST',
            url:'/admin/photocheck/',
            data:{
                'img':$('#propic')[0].files[0],
            },
            processData: false,
            success:function(data){
                alert('photo not curre')
            }
        });
    })
})
