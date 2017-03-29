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