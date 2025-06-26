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

    
    def detailed_calculation(self, seconds):
        """返回详细的计费计算过程"""
        if self.config.billing_mode == "per_minute":
            minutes = seconds / 60.0
            fee = minutes * self.config.fee_per_minute
            return (
                f"计费模式: 按分钟计费\n"
                f"停留时长: {self.format_duration(seconds)}\n"
                f"分钟数: {minutes:.2f}\n"
                f"费率: ¥{self.config.fee_per_minute}/分钟\n"
                f"计算: {minutes:.2f} × {self.config.fee_per_minute} = ¥{fee:.2f}"
            )
        
        elif self.config.billing_mode == "per_hour":
            hours = seconds / 3600.0
            fee = hours * self.config.fee_per_hour
            return (
                f"计费模式: 按小时计费\n"
                f"停留时长: {self.format_duration(seconds)}\n"
                f"小时数: {hours:.2f}\n"
                f"费率: ¥{self.config.fee_per_hour}/小时\n"
                f"计算: {hours:.2f} × {self.config.fee_per_hour} = ¥{fee:.2f}"
            )
        
        elif self.config.billing_mode == "fixed":
            return (
                f"计费模式: 固定费率\n"
                f"固定费用: ¥{self.config.fixed_fee}"
            )
        
        return "未知计费模式"