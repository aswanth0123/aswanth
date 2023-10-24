$(document).ready(function(){
    $('.reg').change(function(){
        var email = $('#email-reg').val()
        var phone = $('#phone-reg').val()
        $.ajax({
            url:'/emailpasswordcheck/',
            data:{
                'email':email,
                'phone':phone
            },
            success:function(item){
                if(item.emailid){
                    $('#error').html(item.emailid)
                    $('#submit-reg').prop('disabled',true)
                }else if(item.phoneno){
                     $('#error').html(item.phoneno)
                     $('#submit-reg').prop('disabled',true)
                }else{
                    $('#error').html('')
                    $('#submit-reg').prop('disabled',false)
                }
            }
        });
    })
    $('.log').change(function(){
        var pass = $('#pass-log').val()
        var email = $('#email-log').val()
        $.ajax({
            url:'/emailpasswordchecklogin/',
            data:{
                'email':email,
                'password':pass
            },
            success:function(item){
                if(item.email){
                     $('#error').html(item.email)
                     $('#submit-log').prop('disabled',true)
                 }else if(item.password){
                     $('#error').html(item.password)
                     $('#submit-log').prop('disabled',true)
                 }else{
                    $('#error').html('')
                    $('#submit-log').prop('disabled',false)
                 }
            }
        });
    })
    $('#oldpass').on('change',function(){
        var pass = $(this).val()
        $.ajax({
            url:'/oldpassconfirm/',
            data:{'pass':pass},
            success:function(data){
                if(data.info){
                    $('#error2').html(data.info)
                    $('#submit-pass').prop('disabled',true)

                }else{
                    $('#error2').html('')
                    $('#submit-pass').prop('disabled',false)
                }
            }
        })
    })



})
