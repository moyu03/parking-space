# core/billing.py

from datetime import timedelta
from core.config import Config

class Billing:
    def __init__(self, config: Config):
        self.config = config

    def calculate_fee(self, seconds):
        if self.config.billing_mode == "per_minute":
            return int(seconds / 60) * self.config.fee_per_minute
        elif self.config.billing_mode == "per_hour":
            return int(seconds / 3600) * self.config.fee_per_hour
        elif self.config.billing_mode == "fixed":
            return self.config.fixed_fee
        else:
            return 0

    def format_duration(self, seconds):
        return str(timedelta(seconds=int(seconds)))
