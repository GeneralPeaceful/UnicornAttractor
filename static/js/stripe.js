$(function() {
    $('#payment-form').submit(function() {
        var form = this;
        var card = {
            number: $('#id_card_number').val(),
            cvc: $('#id_cvv').val(),
            expMonth: $('#id_expiry_month').val(),
            expYear: $('#id_expiry_year').val()
        };
        
        Stripe.createToken(card, function(status, response) {
            if (status === 200) {
                $('#credit-card-errors').hide();
                $('#id_stripe_id').val(response.id);
                
                form.submit();
            }
            else {
                $('#stripe-error-message').text(response.error.message);
                $('#credit-card-errors').show();
                $('#validate_card_btn').attr('disabled', false);
            }
        });
        return false;
    });
});