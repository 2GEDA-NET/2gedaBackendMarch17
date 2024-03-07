TRANSACTION_FLAGS = [("reversed", "Reversed"), ("on-hold", "On Hold")]

PAYMENT_GATEWAY = [
    ("paystack", "Paystack"),  # paystack is the active gateway for now
    # TODO: in case of future reference
    # ("flutterwave", "Flutterwave"),
    # ("stripe", "Stripe"),
]

TRANSACTION_STATUS = [
    ("pending", "Pending"),
    ("success", "Successful"),
    ("failed", "Failed"),
]
