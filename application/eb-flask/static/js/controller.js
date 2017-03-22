Stripe.setPublishableKey('pk_test_PdLFWUk0BeVmaCrviRaoKxjN');

$(function() {
  var $form = $('#payment-form');
  $form.submit(function(event) {
    // Disable the submit button to prevent repeated clicks:
    $form.find('.submit').prop('disabled', true);

    // Request a token from Stripe:
    Stripe.card.createToken($form, stripeResponseHandler);

    // Prevent the form from being submitted:
    // console.log($form)

    return false;
  });
});

function stripeResponseHandler(status, response) {
  // Grab the form:
  var $form = $('#payment-form');

  console.log($form)

  if (response.error) { // Problem!

    // Show the errors on the form:
    console.log(response.error);
    $form.find('.payment-errors').text(response.error.message);
    $form.find('.submit').prop('disabled', false); // Re-enable submission

  } else { // Token was created!

    // Get the token ID:
    var token = response.id;

    // Insert the token ID into the form so it gets submitted to the server:
    $form.append($('<input type="hidden" id="stripeToken" name="stripeToken">').val(token));
    $form.append($('<input type="hidden" id="cartTotal" name="cartTotal">').val(simpleCart.total()));

    //Here is where we would send the form/data/token to the backend to make the Stripe transaction

    console.log(token);

    $form.find('.submit').prop('disabled', false);
    // $form[0].reset();

    $('#helpModal').modal('hide');

    simpleCart.update();
    simpleCart.empty();
    simpleCart.update();

    $form.get(0).submit();
  }
};
