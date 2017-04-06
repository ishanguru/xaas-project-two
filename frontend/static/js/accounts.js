function JSON_stringify(s, emit_unicode)
{
   var json = JSON.stringify(s);
   return emit_unicode ? json : json.replace(/[\u007f-\uffff]/g,
      function(c) {
        return '\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);
      }
   );
}

var accountHandler = {
    jwt_token: null,
    userName: null,
    loginNavElement: $("#loginNavElement"),
    logoutNavElement: $("#logoutNavElement"),
    signUpNavElement: $("#signUpNavElement"),
    usernameNavElement: $("#usernameNavElement")
};

accountHandler.logOut = function () {
    this.jwt_token = null;
    this.userName = null;
    this.usernameNavElement.html("");
    this.usernameNavElement.hide();
    this.logoutNavElement.hide();
    this.signUpNavElement.show();
    this.loginNavElement.show();
};

accountHandler.logIn = function (userName) {
    console.log("hit form handler");
    this.userName = userName;
    this.usernameNavElement.html("<a href='#'>" + userName + "</a>");
    this.usernameNavElement.show();
    this.signUpNavElement.hide();
    this.loginNavElement.hide();
    this.logoutNavElement.show();
};