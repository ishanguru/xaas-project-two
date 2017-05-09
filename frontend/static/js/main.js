/* load in order
    accounts.js
    processing.js
    poll.js
    handlers
 */
//buy

$(document).ready(function() {
    accountHandler.logOut();

    var handlerForItem1 = new ItemHandler(1597,
        "Unity 5.x Cookbook",
        "1597",
        accountHandler,
        'customButton1',
        processingHandler, "1"
    );

    var handlerForItem2 = new ItemHandler(2098,
        "Android Programming for Beginners",
        "20.98",
        accountHandler,
        'customButton2',
        processingHandler, "2"
    );


    $('#loginForm').submit(function (e) {
        e.preventDefault();
          if (processingHandler.checkForOnGoingProcessWithWarning()) {
            return;
          }
        handleLogin($(this).serializeArray().reduce(
            function(accumulater, curr) {
                accumulater[curr.name] = curr.value;
                return accumulater;
            }, {}
        ));
    });
    $('#signUpForm').submit(function (e) {
        e.preventDefault();
          if (processingHandler.checkForOnGoingProcessWithWarning()) {
            return;
          }
        var formData = $(this).serializeArray().reduce(
            function(accumulater, curr) {
                accumulater[curr.name] = curr.value;
                return accumulater;
            }
            , {});
        if(formData["password"] !== formData["passwordCheck"]) {
            alert("Both password entries must match.");
            return;
        } else if (formData["password"].length < 4) {
            alert("Passwords must be at least 4 character in length.");
            return;
        }
        handleSignup(formData);
    });

    // Close Checkout on page navigation:
    window.addEventListener('popstate', function() {
      handlerForItem1.close();
      handlerForItem2.close();
    });

    
    $( "#logoutNavElement" ).click(function() {
        processingHandler.updateStatus("success","You logged out.");
        accountHandler.logOut();
    });
});