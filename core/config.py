import os
import json

class Config:
    def __init__(self):
        self.parking_capacity = 10  # 默认停车场容量
        self.waiting_capacity = 5   # 默认便道容量
        self.billing_mode = "per_minute"
        self.fee_per_minute = 1.0
        self.fee_per_hour = 30.0
        self.fixed_fee = 50.0
        self.history_file = "parking_history.json"
        self.history = self.load_history()
        self.enable_dual_exit = False
        self.dual_exit_settings = {
            "north_waiting_capacity": 10,
            "south_waiting_capacity": 10,
            "optimization_threshold": 0.3
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

    
    def save_to_file(self, filename="config.json"):
        """将配置保存到文件"""
        config_data = {
            "parking_capacity": self.parking_capacity,
            "waiting_capacity": self.waiting_capacity,
            "billing_mode": self.billing_mode,
            "fee_per_minute": self.fee_per_minute,
            "fee_per_hour": self.fee_per_hour,
            "fixed_fee": self.fixed_fee,
            "enable_dual_exit": self.enable_dual_exit,
            "dual_exit_settings": self.dual_exit_settings
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置失败: {str(e)}")
            return False
    
    def load_from_file(self, filename="config.json"):
        """从文件加载配置"""
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            # 更新配置
            self.parking_capacity = config_data.get("parking_capacity", 10)
            self.waiting_capacity = config_data.get("waiting_capacity", 5)
            self.billing_mode = config_data.get("billing_mode", "per_minute")
            self.fee_per_minute = config_data.get("fee_per_minute", 1.0)
            self.fee_per_hour = config_data.get("fee_per_hour", 30.0)
            self.fixed_fee = config_data.get("fixed_fee", 50.0)
            self.enable_dual_exit = config_data.get("enable_dual_exit", False)
            self.dual_exit_settings = config_data.get("dual_exit_settings", {
                "north_waiting_capacity": 10,
                "south_waiting_capacity": 10,
                "optimization_threshold": 0.3
            })
            
            return True
        except Exception as e:
            print(f"加载配置失败: {str(e)}")
            return False