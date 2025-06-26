# core/billing.py

from datetime import timedelta
from core.config import Config

# core/billing.py

class Billing:
    def __init__(self, config: Config):
        self.config = config

    def calculate_fee(self, seconds):
        """计算费用，返回浮点数"""
        if self.config.billing_mode == "per_minute":
            # 使用浮点数计算
            return (seconds / 60.0) * self.config.fee_per_minute
        elif self.config.billing_mode == "per_hour":
            # 使用浮点数计算
            return (seconds / 3600.0) * self.config.fee_per_hour
        elif self.config.billing_mode == "fixed":
            return float(self.config.fixed_fee)
        else:
            return 0.0
  
    def format_duration(self, seconds):
        """格式化时长显示为 HH:MM:SS"""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
