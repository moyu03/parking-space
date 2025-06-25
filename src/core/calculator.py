# src/core/calculator.py
from datetime import datetime
from src.core.constants import PARKING_RATE_PER_MIN

from abc import ABC, abstractmethod

class BillingStrategy(ABC):
    @abstractmethod
    def calculate(self, entry_time, exit_time):
        pass

class BaseBillingStrategy(BillingStrategy):
    def calculate(self, entry_time, exit_time):
        duration = (exit_time - entry_time).total_seconds() / 60
        return round(duration * PARKING_RATE_PER_MIN, 2), round(duration, 1)

def calculate_fee(entry_time, exit_time, strategy=BaseBillingStrategy()):
    return strategy.calculate(entry_time, exit_time)

def format_duration(minutes):
    """
    格式化停留时间
    :param minutes: 停留分钟数
    :return: 格式化的时间字符串 (X小时Y分钟)
    """
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours}小时{mins}分钟" if hours else f"{mins}分钟"