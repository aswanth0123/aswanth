$(document).ready(function(){
    $('.log').change(function(){
        var emailid = $('#email').val()
        var password = $('#pass').val()
        $.ajax({
            url:'/admin/emailpasscheck/',
            data:{
                'email':emailid,'pass':password},
            success:function(item){
                if(item.email){
                    $('#error').html(item.email)
                    $('#btn').prop('disabled',true)
                }else if(item.pass){
                    $('#error').html(item.pass)
                    $('#btn').prop('disabled',true)
                }else{
                    $('#error').html('')
                    $('#btn').prop('disabled',false)
                }
            }
        });
    })
})
