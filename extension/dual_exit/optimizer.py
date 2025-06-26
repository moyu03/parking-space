import time

class ExitOptimizer:
    def __init__(self, parking_lot, waiting_lane):
        self.parking_lot = parking_lot
        self.waiting_lane = waiting_lane
        self.history = []
        self.last_optimize_time = 0
    
    def find_optimal_path(self, car_id):
        """查找车辆最优离开路径"""
        side, index, spot = self.parking_lot.find_car(car_id)
        if not spot:
            return None, "车辆不存在"
        
        # 计算各出口成本
        north_cost = self.calculate_exit_cost("north", side, index)
        south_cost = self.calculate_exit_cost("south", side, index)
        
        # 考虑出口拥堵情况
        north_queue_cost = self.waiting_lane.get_waiting_count("north") * 0.2
        south_queue_cost = self.waiting_lane.get_waiting_count("south") * 0.2
        
        total_north_cost = north_cost + north_queue_cost
        total_south_cost = south_cost + south_queue_cost
        
        # 选择成本较低的出口
        if total_north_cost <= total_south_cost:
            return "north", total_north_cost
        return "south", total_south_cost
    
    def calculate_exit_cost(self, target_exit, current_side, current_index):
        """计算从当前位置到指定出口的成本"""
        if target_exit == current_side:
            # 同侧离开成本
            return current_index * 1.0
        else:
            # 跨侧离开成本
            if current_side == "north":
                return (len(self.parking_lot.north_stack) - current_index) * 0.8 + len(self.parking_lot.south_stack) * 1.2
            else:
                return (len(self.parking_lot.south_stack) - current_index) * 0.8 + len(self.parking_lot.north_stack) * 1.2
    
    def optimize_system(self):
        """系统级优化：平衡两侧负载"""
        # 限制优化频率（至少间隔30秒）
        current_time = time.time()
        if current_time - self.last_optimize_time < 30:
            return False, "优化太频繁，请稍后再试"
        
        self.last_optimize_time = current_time
        
        # 计算南北不平衡度
        north_count = len(self.parking_lot.north_stack)
        south_count = len(self.parking_lot.south_stack)
        total_spots = self.parking_lot.total_spots
        imbalance = abs(north_count - south_count) / total_spots
        
        if imbalance > 0.3:  # 当不平衡度超过30%时触发优化
            moves = 0
            # 限制最大移动数量为3辆
            max_moves = min(3, abs(north_count - south_count) // 2)
            
            if north_count > south_count:
                # 将北端车辆移动到南端（从栈顶开始移动）
                for _ in range(max_moves):
                    if self.parking_lot.north_stack:
                        car_data = self.parking_lot.north_stack.pop()
                        # 更新车辆位置信息
                        new_position = len(self.parking_lot.south_stack) + 1
                        car_data["position"] = f"S{new_position}"
                        self.parking_lot.south_stack.append(car_data)
                        self.record_move(car_data["car"].car_id, "north", "south")
                        moves += 1
            else:
                # 将南端车辆移动到北端（从栈顶开始移动）
                for _ in range(max_moves):
                    if self.parking_lot.south_stack:
                        car_data = self.parking_lot.south_stack.pop()
                        # 更新车辆位置信息
                        new_position = len(self.parking_lot.north_stack) + 1
                        car_data["position"] = f"N{new_position}"
                        self.parking_lot.north_stack.append(car_data)
                        self.record_move(car_data["car"].car_id, "south", "north")
                        moves += 1
            return True, f"系统优化完成，移动了 {moves} 辆车"
        return False, "系统平衡，无需优化"
    
    def record_move(self, car_id, from_side, to_side):
        """记录车辆移动历史"""
        self.history.append({
            "timestamp": time.time(),
            "car_id": car_id,
            "from_side": from_side,
            "to_side": to_side
        })