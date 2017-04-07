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
        var that = this;
        document.getElementById(this.elementId).addEventListener('click', function(e) {
            // Open Checkout with further options:
            e.preventDefault();
            if (processingHandler.checkForOnGoingProcessWithWarning()) {
                return;
            }

            if (accountHandler.jwt_token === null) {
              alert("You must be logged in to purchase something");
            }  else {
                  that.checkOut();
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
                    url: "http://ec2-52-34-67-202.us-west-2.compute.amazonaws.com/payment",
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
