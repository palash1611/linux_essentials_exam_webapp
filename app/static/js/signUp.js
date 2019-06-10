$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                if (response=="{\"message\": \"success\"}")
                    window.location.href = "/objective";
                else
                    console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
