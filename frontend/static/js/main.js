/* load first
    accounts.js
    processing.js
 */


function poll(count, type) {

    function handleFailure(count, data) {
        if (count <= 4) { //try again
            var timeoutID = window.setTimeout(poll(count + 1), 200);
        } else  {
            //todo: probably want to send this info somewhere
            processingHandler.updateStatus("failure", "That operation failed please try again.");
        }
    }


    data["jwt"] = accountHandler.jwt_token;
    data["type"] = type;

    $.ajax({
        type: "POST",
        url: "tbd",
        data: data,
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            if (data["status"] === "success") {
                processingHandler.updateStatus("success", "That operation worked!");
            } else {
                handleFailure(count,data)
            }
        },
        error: function (data) {
            handleFailure(count,data)
        }
    });

}

function login(formData) {
    formData["method"] = "login";
    $.ajax({
        type: "POST",
        url: 'https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/orchestratorV2/ui-api',
        data: JSON.stringify(formData),
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            accountHandler.jwt_token = data.access_token;
            $('#loginModal').modal('hide');
            accountHandler.logIn(formData.username);
        },
        error: function (data) {
            alert("Login Failure")
        }
    });
}

function signUp(formData) { //new acccount
    formData["method"] = "signUp";
    $.ajax({
        type: "POST",
        url: 'https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/orchestratorV2/ui-api',
        data: JSON.stringify(formData),
        success: function(data) {
            $('#signUpModal').modal('hide')
            delete formData["passwordCheck"];
            login(formData);
        },
        error: function (data) {
            alert("Could not sign up. Username may be taken.");
        }
    });
}

//buy
var handler1 = StripeCheckout.configure({
  key: 'pk_test_mLVxfSZ0XoplPi6EppPDVic9',
  image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
  locale: 'auto',
  token: function(token) {
      token["amount"] = 1597;
      token["method"] = "charge";
      token["jwt"] = accountHandler.jwt_token;
    $.ajax({
            type: "POST",
            url: "https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/orchestratorV2/ui-api",
            headers: { "Authorization" : "JWT " + accountHandler.jwt_token },
            data: JSON.stringify(token),
            success: function(data) {
                alert("Purchase successful for " + data["amount"] + " cents.");
            },
            error: function(data) {
                console.log("failure");
                alert("You must be logged in!");
            }
        });
  }
});
var handler2 = StripeCheckout.configure({
  key: 'pk_test_mLVxfSZ0XoplPi6EppPDVic9',
  image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
  locale: 'auto',
  token: function(token) {
    token["amount"] = 2098;
    token["method"] = "charge";
    token["jwt"] = accountHandler.jwt_token;
    $.ajax({
            type: "POST",
            url: "https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/orchestratorV2/ui-api",
            headers: { "Authorization" : "JWT " + accountHandler.jwt_token },
            data: JSON.stringify(token),
            success: function(data) {
                 alert("Purchase successful for " + data["amount"] + " cents.");
            },
            error: function(data) {
                console.log("failure");
                alert("You must be logged in!");
            }
        });
  }
});

function onGoingProcess() {
    if (!(processingHandler.status == "success" ||
              processingHandler.status == "clear")) {
              alert("Wait for ongoing process!")
        return true;
        }
    return false;
}

$(document).ready(function() {
    accountHandler.logOut();

    $('#loginForm').submit(function (e) {
        e.preventDefault();
        if (onGoingProcess()) {
            return;
        }
        login($(this).serializeArray().reduce(
            function(accumulater, curr) {
                accumulater[curr.name] = curr.value;
                return accumulater;
            }, {}));
    });
    $('#signUpForm').submit(function (e) {
        e.preventDefault();
        if (onGoingProcess()) {
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
        signUp(formData);
    });
    
    document.getElementById('customButton1').addEventListener('click', function(e) {
      // Open Checkout with further options:
          if (onGoingProcess()) {
            return;
          }
          if (accountHandler.jwt_token === null) {
              alert("You must be logged in to purchase something");
          } else {
              handler1.open({
                name: 'Unity 5.x Cookbook',
                description: '15.97',
                amount: 1597
              });
          }
          e.preventDefault();
     });
     
         document.getElementById('customButton2').addEventListener('click', function(e) {
      // Open Checkout with further options:
          if (onGoingProcess()) {
            return;
          }
        if (accountHandler.jwt_token === null) {
              alert("You must be logged in to purchase something");
          }  else {
              handler2.open({
                name: 'Android Programming for Beginners',
                description: '20.98',
                amount: 2098
              });
          }
          e.preventDefault();
     });

    // Close Checkout on page navigation:
    window.addEventListener('popstate', function() {
      handler1.close();
      handler2.close();
    });

    
    $( "#logoutNavElement" ).click(function() {
        accountHandler.logOut();
    });
    



});