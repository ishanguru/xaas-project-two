class ItemHandler {
    constructor(amount, name, description, accountHandler) {
        this.amount = amount;
        this.name = name;
        this.description = description;
        this.accountHandler = accountHandler;
        this.checkOutHandler =
            this.checkOutHandlerDefaultConfigFactory(this.amount);
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
console.log(accountHandler);
var handlerForItem1 = new ItemHandler(1597, "Unity 5.x Cookbook", "1597", accountHandler);
var handlerForItem2 = new ItemHandler(2098, "Android Programming for Beginners", "20.98", accountHandler);
