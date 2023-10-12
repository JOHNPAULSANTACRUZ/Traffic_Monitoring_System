$(document).ready(function() { 
    $('form.').on('submit',function(event){
        $.ajax({
            data:{
                username: $('#usernameInput').val(),
                email: $('#emailInput').val(),
                password:$('#passwordInput').val(),
                confirmPassword:$('#confirmPasswordInput').val()
            },
            type:'/POST',
            url:'/success_register'
        })
        .done(function(data){
            if(data.error){
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            }
            else{
                $('#successAlert').text(data.success).show();
                $('#errorAlert').hide();
            }
        });
        event.preventDefault();
    })
});
   