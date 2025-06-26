class DualWaitingLane:
    def __init__(self, capacity=20):
        self.north_queue = []  # 北便道队列
        self.south_queue = []  # 南便道队列
        self.capacity = capacity
    
    
    def is_car_exists(self, car_id):
        """检查便道中是否存在指定车牌号的车辆"""
        for item in self.north_queue:
            if item["car"].car_id == car_id:
                return True
        
        for item in self.south_queue:
            if item["car"].car_id == car_id:
                return True
        
        return False
    
    def enqueue(self, car, arrival_time):
        """车辆进入便道，选择最短队列"""
        if len(self.north_queue) + len(self.south_queue) >= self.capacity:
            return False, "便道已满"
        
        # 选择较短的队列
        if len(self.north_queue) <= len(self.south_queue):
            position = len(self.north_queue) + 1
            self.north_queue.append({
                "car": car,
                "arrival_time": arrival_time,
                "position": f"NQ{position}"
            })
            return True, f"北便道{position}"
        else:
            position = len(self.south_queue) + 1
            self.south_queue.append({
                "car": car,
                "arrival_time": arrival_time,
                "position": f"SQ{position}"
            })
            return True, f"南便道{position}"
    
    def dequeue(self, side=None):
        """从便道取出车辆，优先选择指定侧"""
        if side == "north" and self.north_queue:
            return self.north_queue.pop(0)
        elif side == "south" and self.south_queue:
            return self.south_queue.pop(0)
        
        # 未指定侧时，选择非空队列
        if self.north_queue:
            return self.north_queue.pop(0)
        elif self.south_queue:
            return self.south_queue.pop(0)
        return None
    
    def get_status(self):
        """获取便道状态"""
        return {
            "north": [item.copy() for item in self.north_queue],
            "south": [item.copy() for item in self.south_queue],
            "total": len(self.north_queue) + len(self.south_queue)
        }
    
    def get_waiting_count(self, side=None):
        """获取等待车辆数"""
        if side == "north":
            return len(self.north_queue)
        elif side == "south":
            return len(self.south_queue)
        return len(self.north_queue) + len(self.south_queue)