from extension.dual_exit.parking import DualExitParkingLot
from extension.dual_exit.lane import DualWaitingLane
from extension.dual_exit.optimizer import ExitOptimizer
from core.parking import ParkingLot, WaitingLane
import time

class DualSystemAdapter:
    def __init__(self, config, old_parking=None, old_waiting=None, billing=None, log_callback=None):
        self.config = config
        self.billing = billing
        self.log = log_callback or (lambda msg, level: print(f"[{level}] {msg}"))
        self.parking_lot = DualExitParkingLot(config.parking_capacity)
        self.waiting_lane = DualWaitingLane(config.waiting_capacity * 2)
        self.optimizer = ExitOptimizer(self.parking_lot, self.waiting_lane)
        
        if old_parking and old_waiting:
            try:
                self.migrate_from_old_system(old_parking, old_waiting)
            except Exception as e:
                self.log(f"迁移旧系统数据失败: {str(e)}", "error")
    
    def migrate_from_old_system(self, old_parking, old_waiting):
        """从旧系统迁移数据"""
        # 迁移停车场
        for car in old_parking.stack:
            success, position = self.parking_lot.enter(car, car.enter_time)
            if not success:
                self.log(f"警告: 无法迁移车辆 {car.car_id} 到双门系统停车场", "warning")
        
        # 迁移便道
        for car in old_waiting.queue:
            success, position = self.waiting_lane.enqueue(car, car.enter_time)
            if not success:
                self.log(f"警告: 无法迁移车辆 {car.car_id} 到双门系统便道", "warning")
    
   
    def is_car_exists(self, car_id):
        """检查车牌号是否已存在"""
        # 检查停车场
        if self.parking_lot.find_car(car_id)[2]:
            return True
        
        # 检查便道
        return self.waiting_lane.is_car_exists(car_id)
    
    def enter(self, car):
        """车辆进入系统"""
        current_time = time.time()
        try:
            # 检查车牌号是否已存在
            if self.is_car_exists(car.car_id):
                return "EXISTS", "车牌号已存在", current_time
            
            # 尝试进入停车场
            success, position = self.parking_lot.enter(car, current_time)
            if success:
                self.log(f"车辆 {car.car_id} 停入{position}", "success")
                return "PARKED", position, current_time
            
            # 停车场满，进入便道
            success, position = self.waiting_lane.enqueue(car, current_time)
            if success:
                self.log(f"车辆 {car.car_id} 在{position}等待", "info")
                return "IN_SIDE_ROAD", position, current_time
            
            self.log(f"车辆 {car.car_id} 被拒绝: 系统已满", "warning")
            return "REJECTED", "系统已满", current_time
        except Exception as e:
            self.log(f"车辆进入失败: {str(e)}", "error")
            return "ERROR", "系统错误", current_time
    
    def leave(self, car_id):
        """车辆离开系统"""
        exit_time = time.time()
        try:
            success, result = self.parking_lot.leave(car_id, exit_time)
            
            if not success:
                self.log(f"车辆 {car_id} 离开失败: {result}", "error")
                return "FAILURE", result
            
            # 添加历史记录
            self.config.add_history(
                car_id, 
                result["entry_time"], 
                exit_time, 
                self.billing.calculate_fee(result["duration"])
            )
            
            # 从便道补充车辆
            side = "north" if result["position"].startswith("N") else "south"
            next_car = self.waiting_lane.dequeue(side)
            
            result_data = {"departed": result}
            if next_car:
                # 新车辆进入停车场
                self.parking_lot.enter(next_car["car"], exit_time)
                result_data["entered"] = next_car
                self.log(f"车辆 {next_car['car'].car_id} 已从便道移入停车场", "info")
            
            self.log(f"车辆 {car_id} 已成功离开", "success")
            return "SUCCESS", result_data
        except Exception as e:
            self.log(f"车辆离开失败: {str(e)}", "error")
            return "ERROR", "系统错误"
    
    def get_optimal_path(self, car_id):
        """获取最优离开路径"""
        try:
            exit_side, cost = self.optimizer.find_optimal_path(car_id)
            if exit_side:
                self.log(f"车辆 {car_id} 推荐出口: {exit_side.upper()}, 成本: {cost:.1f}", "info")
                return exit_side, cost
            return None, "车辆不存在"
        except Exception as e:
            self.log(f"获取最优路径失败: {str(e)}", "error")
            return None, "系统错误"
    
    def optimize_system(self):
        """执行系统优化"""
        try:
            success, message = self.optimizer.optimize_system()
            if success:
                self.refresh_status()
            return success, message
        except Exception as e:
            self.log(f"系统优化失败: {str(e)}", "error")
            return False, "系统优化失败"
    
    def get_status(self):
        """获取系统状态"""
        return {
            "parking": self.parking_lot.get_status(),
            "waiting": self.waiting_lane.get_status()
        }
    
    def refresh_status(self):
        """刷新状态（供外部调用）"""
        self.optimizer.optimize_system()  # 每次刷新时尝试优化