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
            var timeoutID = window.setTimeout(pollCharge(count + 1), 200);
        } else  {
            //todo: probably want to send this info somewhere
            processingHandler.updateStatus("error", "That operation failed please try again.");
        }
    }
    var data = {};
    data["jwt"] = accountHandler.jwt_token;
    data["type"] = "chargeQuery";

    $.ajax({
        type: "POST",
        url: "https://ec2-52-34-67-202.us-west-2.compute.amazonaws.com/getpayment",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        success: function(reply) {
            console.log(reply)
            if (data["status"] === "success") {
                processingHandler.updateStatus("success", "That operation worked!");
            } else {
                handleFailure(count,reply)
            }
        },
        error: function (reply) {
            handleFailure(count,reply)
        }
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

    $.ajax({
        type: "POST",
        url: "https://zk84kq0q36.execute-api.us-east-1.amazonaws.com/prod/login",
        data: JSON.stringify(info),
        contentType: "application/json; charset=utf-8",
        success: function(reply) {
            reply = JSON_stringify(reply, true);
            reply = JSON.parse(reply)
            if (reply["status"] === "success") {
                console.log("success")
              accountHandler.jwt_token = reply.access_token;
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
        type: "POST",
        url: "https://zk84kq0q36.execute-api.us-east-1.amazonaws.com/prod/signup",
        data: JSON.stringify(info),
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            if (data["status"] === "success") {
              delete info["passwordCheck"];
              handleLogin(info);
            } else {
                handleFailure(count,data)
            }
        },
        error: function (data) {
            handleFailure(count,data)
        }
    });
}
