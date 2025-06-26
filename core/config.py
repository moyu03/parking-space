# core/config.py

import os
import json

class Config:
    def __init__(self):
        self.parking_capacity = 5
        self.waiting_capacity = 3
        self.billing_mode = "per_minute"  # or "per_hour", "fixed"
        self.fee_per_minute = 1
        self.fee_per_hour = 30
        self.fixed_fee = 50
        self.history_file = "parking_history.json"
        self.history = self.load_history()
        self.enable_dual_exit = False  # 是否启用双向出口系统
        self.dual_exit_settings = {
            "north_waiting_capacity": 10,
            "south_waiting_capacity": 10,
            "optimization_threshold": 0.3  # 优化触发阈值
        }
    
    def enable_dual_exit_system(self, enable=True):
        """启用/禁用双向出口系统"""
        self.enable_dual_exit = enable
        
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

     
    def load_history(self):
        """加载停车历史记录"""
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_history(self):
        """保存停车历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def add_history(self, car_id, enter_time, exit_time, fee):
        """添加停车记录"""
        self.history.append({
            "car_id": car_id,
            "enter_time": enter_time,
            "exit_time": exit_time,
            "fee": fee
        })
        self.save_history()
    
    def clear_history(self):
        """清空停车历史记录"""
        self.history = []
        self.save_history()
