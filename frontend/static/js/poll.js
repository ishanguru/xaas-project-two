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