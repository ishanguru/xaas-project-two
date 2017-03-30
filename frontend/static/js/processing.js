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
};

processingHandler.updateStatus = function (status, msg) {
    this.status = status;
    this.displayHandler[this.status](msg);

};

function onGoingProcess() {
    if (!(processingHandler.status == "success" ||
        processingHandler.status == "clear")) {
        alert("Wait for ongoing process!");
        return true;
    }
    return false;
}