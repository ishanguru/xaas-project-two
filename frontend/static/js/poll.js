function startPollCharge() {
    processingHandler.updateStatus("waiting",null);
    pollCharge(0);
}

function startPollLogin(info) {
    processingHandler.updateStatus("waiting",null);
    pollLogin(0, info);
}

function startPollSignup(info) {
    processingHandler.updateStatus("waiting",null);
    pollSignup(0, info);
}

function pollCharge(count) {

    function handleFailure(count, data) {
        if (count <= 4) { //try again
            var timeoutID = window.setTimeout(pollCharge(count + 1, info), 200);
        } else  {
            //todo: probably want to send this info somewhere
            processingHandler.updateStatus("error", "That operation failed please try again.");
        }
    }
    var data = {};
    data["jwt"] = accountHandler.jwt_token;
    data["type"] = "charge";

    $.ajax({
        type: "GET",
        url: "https://b98im1pkw9.execute-api.us-east-1.amazonaws.com/prod/checkqueue",
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

function pollLogin(count, info) {
    console.log(info);
    info["type"] = "login";

    function handleFailure(count, data) {
        if (count <= 4) { //try again
            var timeoutID = window.setTimeout(pollLogin(count + 1, info), 200);
        } else  {
            //todo: probably want to send this info somewhere
            processingHandler.updateStatus("error", "That operation failed please try again.");
        }
    }

    $.ajax({
        type: "GET",
        url: "https://b98im1pkw9.execute-api.us-east-1.amazonaws.com/prod/checkqueue",
        data: info,
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            if (data["status"] === "success") {
              accountHandler.jwt_token = data.access_token;
              accountHandler.logIn(formData.username);
            } else {
                handleFailure(count,data)
            }
        },
        error: function (data) {
            handleFailure(count,data)
        }
    });
}

function pollSignup(count, info) {
    info["type"] = "signup";

    function handleFailure(count, data) {
        if (count <= 4) { //try again
            var timeoutID = window.setTimeout(pollSignup(count + 1, info), 200);
        } else  {
            //todo: probably want to send this info somewhere
            processingHandler.updateStatus("error", "That operation failed please try again.");
        }
    }

    $.ajax({
        type: "GET",
        url: "https://b98im1pkw9.execute-api.us-east-1.amazonaws.com/prod/checkqueue",
        data: info,
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            if (data["status"] === "success") {
              delete formData["passwordCheck"];
              login(formData);
            } else {
                handleFailure(count,data)
            }
        },
        error: function (data) {
            handleFailure(count,data)
        }
    });
}
