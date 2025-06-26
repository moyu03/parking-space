# core/config.py

class Config:
    def __init__(self):
        self.parking_capacity = 5
        self.waiting_capacity = 3
        self.billing_mode = "per_minute"  # or "per_hour", "fixed"
        self.fee_per_minute = 1
        self.fee_per_hour = 30
        self.fixed_fee = 50

    def set_capacity(self, parking, waiting):
        self.parking_capacity = parking
        self.waiting_capacity = waiting

    def set_billing(self, mode, amount):
        self.billing_mode = mode
        if mode == "per_minute":
            self.fee_per_minute = amount
        elif mode == "per_hour":
            self.fee_per_hour = amount
        elif mode == "fixed":
            self.fixed_fee = amount
