
//globals

var jwt_token = null; //recived from server, passed back doing payment

var accountDisplayHandler = {
    userName: null,
    loginNavElement: $("#loginNavElement"),
    logoutNavElement: $("#logoutNavElement"),
    signUpNavElement: $("#signUpNavElement"),
    usernameNavElement: $("#usernameNavElement")
};

accountDisplayHandler.logOut = function () {
    jwt_token = null;
    this.userName = null;
    this.usernameNavElement.html("")
    this.usernameNavElement.hide();
    this.logoutNavElement.hide();
    this.signUpNavElement.show();
    this.loginNavElement.show();

}


accountDisplayHandler.logIn = function (userName) {
    console.log("hit form handler");
    this.userName = userName;
    this.usernameNavElement.html("<a href='#'>" + userName + "</a>");
    this.usernameNavElement.show();
    this.signUpNavElement.hide();
    this.loginNavElement.hide();
    this.logoutNavElement.show();
}
function InactivityTimer(delay) {

  // private instance var
  var timeout;

  // private functions
  function my_logout() {
    console.log("inhere")
    alert("you've been logged out");
    accountDisplayHandler.logOut();
  }

  function reset() {
    stop();
    start();
  }

  function start() {
    if (!timeout) {
      timeout = setTimeout(my_logout, delay || 20000);
    }
  }

  function stop() {
    if (timeout) {
      clearTimeout(timeout);
      timeout = null;
    }
  }

  // export public api
  this.start = start;
  this.stop  = stop;
  this.reset = reset;

  // init
  document.addEventListener("mousemove", reset);
  document.addEventListener("keypress",  reset);
}

function login(formData) {
    $.ajax({
        type: "POST",
        url: '/auth',
        data: JSON.stringify(formData),
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            jwt_token = data.access_token;
            $('#loginModal').modal('hide');
            accountDisplayHandler.logIn(formData.username);
            console.log('Time started')
            var timer = new InactivityTimer(20000);
            timer.stop();
            timer.start();
        },
        error: function (data) {
            alert("Login Failure")
        }
    });
}

function signUp(formData) { //new acccount
    $.ajax({
        type: "POST",
        url: '/signUp',
        data: formData,
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
    $.ajax({
            type: "POST",
            url: "/charge",
            headers: { "Authorization" : "JWT " + jwt_token },
            data: token,
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
    $.ajax({
            type: "POST",
            url: "/charge",
            headers: { "Authorization" : "JWT " + jwt_token },
            data: token,
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



$(document).ready(function() {
    accountDisplayHandler.logOut();

    $('#loginForm').submit(function (e) {
        e.preventDefault();
        login($(this).serializeArray().reduce(
            function(accumulater, curr) {
                accumulater[curr.name] = curr.value;
                return accumulater;
            }, {}));
    });
    $('#signUpForm').submit(function (e) {
        e.preventDefault();
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
            alert("Passwords must be at least 5 character in length.");
            return;
        }
        signUp(formData);
    });
    
    document.getElementById('customButton1').addEventListener('click', function(e) {
      // Open Checkout with further options:
          if (jwt_token === null) {
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
        if (jwt_token === null) {
              alert("You must be logged in to purchase something");
          } else {
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
        accountDisplayHandler.logOut();
    });
    



});