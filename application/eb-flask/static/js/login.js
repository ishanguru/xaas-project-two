$(function() {
  var $form = $('#login-form');

  $form.submit(function(event) {

    // event.preventDefault();

    user = event.target.inputEmail.value;
    password = event.target.inputPassword.value;

    // logintype = $(document.activeElement)[0].id;

    // The below email and password can be sent to the server to authenticate (or something like that)

    var data = {};

    data.user = user;
    data.password = password;

    // console.log(logintype)

    // if (logintype == "signin") {
    //   $.ajax({
    //     url: "/login",
    //     data:data,
    //     success: function(response){
    //         console.log(response);
    //         //check if no, then it
    //     }
    //   });
    // }
    // else {
    //   $.ajax({
    //     url: "/register",
    //     data:data,
    //     success: function(response){
    //         console.log(response);
    //         //check if no, then it
    //     }
    // });
    // }

    console.log(data);

    $form.get(0).submit();

    return true;
  });
});

$(function() {
  var $form = $('#register-form');

  $form.submit(function(event) {

    // event.preventDefault();

    user = event.target.inputEmail.value;
    password = event.target.inputPassword.value;

    var data = {};

    data.user = user;
    data.password = password;

    console.log(data);

    $form.get(0).submit();

    return true;
  });
});

function buttonClicked() {

  $('#login-form').hide();
  $('#registerbutton').hide();
  $('#register-form').show();
  $('#signinbutton').show();

};


function button2Clicked() {

  $('#register-form').hide();
  $('#signinbutton').hide();
  $('#login-form').show();
  $('#registerbutton').show();
};