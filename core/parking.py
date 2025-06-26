import time
from collections import deque

class Car:
    """汽车实体类"""
    def __init__(self, car_id):
        self.car_id = car_id
        self.enter_time = time.time()

    def get_duration(self):
        """计算停留时间"""
        return time.time() - self.enter_time

class ParkingLot:
    """停车场类，使用栈结构实现"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.stack = []  # 主停车场栈

    def is_full(self):
        """检查停车场是否已满"""
        return len(self.stack) >= self.capacity

    def arrive(self, car: Car):
        """车辆进入停车场"""
        if self.is_full():
            return False
        self.stack.append(car)
        return True

    def depart(self, car_id):
        """车辆离开停车场，实现让路机制"""
        temp_stack = []  # 存储让路车辆的临时栈
        moved_cars = []  # 记录所有被移动的车辆
        found = False
        target = None
        
        # 查找目标车辆并让路
        while self.stack:
            current = self.stack.pop()
            if current.car_id == car_id:
                found = True
                target = current
                break
            else:
                # 将让路车辆存入临时栈并记录
                temp_stack.append(current)
                moved_cars.append(current)  # 记录所有让路车辆
        
        # 未找到车辆
        if not found:
            # 恢复让路车辆到停车场
            while temp_stack:
                self.stack.append(temp_stack.pop())
            return None, []  # 返回目标车辆和让路车辆列表
        
        # 将让路车辆按原次序放回停车场
        while temp_stack:
            self.stack.append(temp_stack.pop())
        
        return target, moved_cars  # 返回目标车辆和让路车辆列表

    def current_state(self):
        """获取当前停车场状态"""
        return [(car.car_id, car.enter_time) for car in self.stack]

class WaitingLane:
    """便道类，使用队列结构实现"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = deque()

    def is_full(self):
        """检查便道是否已满"""
        return len(self.queue) >= self.capacity

    def enqueue(self, car: Car):
        """车辆进入便道"""
        if self.is_full():
            return False
        self.queue.append(car)
        return True

    def dequeue(self):
        """车辆离开便道"""
        if not self.queue:
            return None
        return self.queue.popleft()

    def current_state(self):
        """获取当前便道状态"""
        return [(car.car_id, car.enter_time) for car in self.queue]