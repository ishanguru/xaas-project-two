var processingDisplayHandler = {
   processing: false,
   processingDisplayElement: $("#processingDisplay")
};

processingDisplayHandler.waiting = function (msg) {
    this.processingDisplayElement.text("Processing...");
    this.processingDisplayElement.css("color","yellow");
    this.processingDisplayElement.show();
};

processingDisplayHandler.error = function (error) {
    this.processingDisplayElement.text("Error: " + error);
    this.processingDisplayElement.css("color","red");
    this.processingDisplayElement.show();
};

processingDisplayHandler.success = function (msg) {
    this.processingDisplayElement.text("Success: " + msg);
    this.processingDisplayElement.css("color","green");
    this.processingDisplayElement.show();
};

processingDisplayHandler.clear = function () {
    this.processingDisplayElement.hide()
};

var processingHandler = {
    status : "clear",
    displayHandler : processingDisplayHandler,
    get onGoingProcess() {
        return !(processingHandler.status == "success" ||
               processingHandler.status == "clear" ||
                processingHandler.status == "error");
    }
};

processingHandler.updateStatus = function (status, msg) {
    this.status = status;
    this.displayHandler[this.status](msg);
};

processingHandler.checkForOnGoingProcessWithWarning =
    function (warning) {
        if (!processingHandler.onGoingProcess) {
            return false;
        }
        if (warning != undefined) {
            alert(warning);
            return true;
        }
        alert("Wait for ongoing process!")
        return true;
    };
