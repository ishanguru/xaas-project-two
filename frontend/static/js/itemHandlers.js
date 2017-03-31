class ItemHandler {
    constructor(amount, name, description, accountHandler, elementId, processingHandler) {
        this.amount = amount;
        this.name = name;
        this.description = description;
        this.accountHandler = accountHandler;
        this.elementId = elementId;
        this.processingHandler = processingHandler;
        this.checkOutHandler =
            this.checkOutHandlerDefaultConfigFactory(this.amount);
        document.getElementById(this.elementId).addEventListener('click', function(e) {
            // Open Checkout with further options:
            e.preventDefault();
            if (this.processingHandler.checkForOnGoingProcessWithWarning()) {
                return;
            }

            if (this.accountHandler.jwt_token === null) {
              alert("You must be logged in to purchase something");
            }  else {
                  this.checkOut();
            }
         });
    }

    close() {
        this.checkOutHandler.close();
    }
    //construction occuring during checkout as jwt may change.

    checkOut() {
        //todo reconfigure now as to get the newest JWT token?
        //todo use statics
        this.checkOutHandler =
            this.checkOutHandlerDefaultConfigFactory(this.amount);

        //then open
        this.checkOutHandler.open({
            name: this.name,
            description: this.description,
            amount: this.amount
        });
    }

     checkOutHandlerFactory(configAttributes, tokenItems) {
        var that = this;
        return StripeCheckout.configure({
            key: configAttributes["key"],
            image: configAttributes["image"],
            locale: configAttributes["locale"],
            token: function (token) {
                Object.assign(token, tokenItems);
                $.ajax({
                    type: "POST",
                    url: "https://ibw5jd0k4c.execute-api.us-east-1.amazonaws.com/orchestratorV2/ui-api",
                    headers: {"Authorization": "JWT " + that.accountHandler.jwt_token},
                    data: JSON.stringify(Object.assign(token, {"jwt": that.accountHandler.jwt_token})),
                    success: function (data) {
                        startPollCharge();
                    },
                    error: function (data) {
                        alert("You must be logged in!");
                    }
                });
            }
        })
    }

     checkOutHandlerDefaultConfigFactory(amount) {
        return this.checkOutHandlerFactory({
            "key": 'pk_test_mLVxfSZ0XoplPi6EppPDVic9',
            "image": 'https://stripe.com/img/documentation/checkout/marketplace.png',
            "locale": 'auto'
        }, {
            "method": "charge",
            "amount": amount
        });
    }
}

