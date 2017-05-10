function startPollCharge(info) {
    processingHandler.updateStatus("waiting",null);
    pollCharge(0, info);
}

function startPollLogin(info) {
    processingHandler.updateStatus("waiting",null);
    pollLogin(0, info);
}

function startPollSignup(info) {
    processingHandler.updateStatus("waiting",null);
    pollSignup(0, info);
}

function pollCharge(count,info) {

    function handleFailure(count, data) {
        if (count <= 4) { //try again
            var timeoutID = window.setTimeout(pollCharge(count + 1,info), 200);
        } else  {
            //todo: probably want to send this info somewhere
            processingHandler.updateStatus("error", "That operation failed please try again.");
        }
    }
    var data = {};
    data["jwt"] = accountHandler.jwt_token;
    data["type"] = "chargeQuery";
    data["aid"] = info;
    console.log(data);
    $.ajax({
        type: "GET",
        url: "https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/p3v1/orders/" + data["aid"],
        success: function(reply) {
            reply = JSON.parse(reply);
            console.log(reply);
            if (reply["status"] === "success") {
                processingHandler.updateStatus("success", "That operation worked!");
            } else {
                handleFailure(count,reply)
            }
        },
        error: function (reply) {
            handleFailure(count,reply)
        },
        timeout: 10000
    });
}

function pollLogin(count, info) {
    info["type"] = "loginQuery";

    function handleFailure(count, data) {
        if (count <= 4) { //try again
            var timeoutID = window.setTimeout(pollLogin(count + 1, info), 200);
        } else  {
            //todo: probably want to send this info somewhere
            processingHandler.updateStatus("error", "That operation failed please try again.");
        }
    }

    info["email"] = info["username"];

    $.ajax({
        type: "GET",
        url: "https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/p3v1/users/login/" + info.aid,
        // data: JSON.stringify(info),
        // contentType: "application/json; charset=utf-8",
        success: function(reply) {
            reply = JSON_stringify(reply, true);
            reply = JSON.parse(reply);
            console.log("reply");
            console.log(reply);
            if (reply["status"] === "success") {
                console.log("success");
              accountHandler.jwt_token = reply.jwt;
              accountHandler.logIn(info.username);
              processingHandler.updateStatus("success", "You are logged in. Now buy something or get out!")
            } else {
                handleFailure(count,reply)
            }
        },
        error: function (reply) {
            handleFailure(count,reply)
        }
    });
}

function pollSignup(count, info) {
    info["type"] = "signupQuery";

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
        url: "https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/p3v1/users/" + info.aid,
        success: function(data) {
            if (data["name"]) {
              delete info["passwordCheck"];
              processingHandler.updateStatus("success", "Check your email buddy.")
            } else {
                handleFailure(count,data)
            }
        },
        error: function (data) {
            handleFailure(count,data)
        }
    });
}
