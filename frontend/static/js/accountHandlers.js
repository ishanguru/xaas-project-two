function handleLogin(formData) {
    formData["method"] = "login";
    if (!formData["username"]) {
        formData["username"] = formData["Email"];
    }
    $('#loginModal').modal('hide');
    console.log("login");
    $.ajax({
        type: "POST",
        url: 'https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/exp4/login',
        data: JSON.stringify(formData),
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        success: function(data) {
          var info = {
            aid: data,
            username: formData.username,
            password: formData.password
          };
          startPollLogin(info)
        },
        error: function (data) {
            alert("Login Failure")
        }
    });
}

function handleSignup(formData) { //new acccount
    formData["method"] = "signup";
    formData["username"] = formData["Email"];
    $('#signUpModal').modal('hide');
    $.ajax({
        type: "POST",
        url: 'https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/exp4/signup',
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(formData),
        success: function(data) {
          var info = {
            aid: data,
            username: formData.username,
            password: formData.password
          };
          startPollSignup(info);
        },
        error: function (data) {
            alert("Could not sign up. Username may be taken.");
        }
    });
}
