import time

class DualExitParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.north_stack = []  # 北端停车场（栈结构）
        self.south_stack = []  # 南端停车场（栈结构）
        self.total_spots = capacity
        self.occupied = 0

    
    def is_car_exists(self, car_id):
        """检查停车场中是否存在指定车牌号的车辆"""
        for spot in self.north_stack:
            if spot["car"].car_id == car_id:
                return True
        
        for spot in self.south_stack:
            if spot["car"].car_id == car_id:
                return True
        
        return False
    
    def enter(self, car, entry_time):
        """车辆进入，自动选择最优入口"""
        if self.occupied >= self.total_spots:
            return False, "停车场已满"
        
        # 选择车辆较少的入口
        if len(self.north_stack) <= len(self.south_stack):
            position = f"N{len(self.north_stack)+1}"
            self.north_stack.append({
                "car": car,
                "entry_time": entry_time,
                "position": position
            })
        else:
            position = f"S{len(self.south_stack)+1}"
            self.south_stack.append({
                "car": car,
                "entry_time": entry_time,
                "position": position
            })
        
        self.occupied += 1
        return True, position
    
    def find_car(self, car_id):
        """查找车辆位置"""
        for i, spot in enumerate(self.north_stack):
            if spot["car"].car_id == car_id:
                return "north", i, spot
        
        for i, spot in enumerate(self.south_stack):
            if spot["car"].car_id == car_id:
                return "south", i, spot
        
        return None, -1, None
    
    def leave(self, car_id, exit_time):
        """车辆离开，选择最优出口"""
        side, index, spot = self.find_car(car_id)
        if not spot:
            return False, "车辆不存在"
        
        # 计算让路成本（上方车辆数量）
        move_cost = 0
        if side == "north":
            # 北端车辆从北出口离开
            move_cost = len(self.north_stack) - index - 1
            # 移除车辆
            self.north_stack.pop(index)
            # 下方车辆上移
            for i in range(index, len(self.north_stack)):
                self.north_stack[i]["position"] = f"N{i+1}"
        else:
            # 南端车辆从南出口离开
            move_cost = len(self.south_stack) - index - 1
            self.south_stack.pop(index)
            for i in range(index, len(self.south_stack)):
                self.south_stack[i]["position"] = f"S{i+1}"
        
        self.occupied -= 1
        duration = exit_time - spot["entry_time"]
        return True, {
            "car": spot["car"],
            "position": spot["position"],
            "entry_time": spot["entry_time"],
            "exit_time": exit_time,
            "duration": duration,
            "move_cost": move_cost
        }
    
    def get_status(self):
        """获取停车场状态"""
        return {
            "north": [spot.copy() for spot in self.north_stack],
            "south": [spot.copy() for spot in self.south_stack],
            "occupied": self.occupied,
            "capacity": self.total_spots
        }
    
    def get_occupancy_rate(self):
        """获取占用率"""
        return self.occupied / self.total_spots * 100