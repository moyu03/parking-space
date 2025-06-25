from datetime import datetime
import time
from src.core.calculator import calculate_fee, format_duration
from src.core.constants import MAX_PARKING_SPOTS

from abc import ABC, abstractmethod

class ParkingLotObserver(ABC):
    @abstractmethod
    def on_parking_change(self, parking_data):
        pass

class ParkingLotService:
    def __init__(self, capacity=MAX_PARKING_SPOTS):
        self.capacity = capacity
        self.stack = []
        self.temp_stack = []
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def get_parking_data(self):
        return {
            'current': len(self.stack),
            'capacity': self.capacity,
            'vehicles': [
                {
                    'plate': str(plate), 
                    'minutes': int((datetime.now() - entry_time).total_seconds() // 60)
                }
                for plate, entry_time in self.stack
            ]
        }

    def notify_observers(self):
        data = self.get_parking_data()
        for observer in self.observers:
            observer.on_parking_change(data)

class ParkingLot(ParkingLotService):
    def __init__(self, capacity=MAX_PARKING_SPOTS):
        super().__init__(capacity)
    
    def enter(self, car_id):
        """车辆进入停车场"""
        entry_time = datetime.now()
        if len(self.stack) >= self.capacity:
            return False, entry_time, "停车场已满"
        
        # 创建车辆记录 (车牌, 进入时间, 位置)
        position = len(self.stack) + 1
        self.stack.append( (car_id, entry_time) )
        self.notify_observers()
        return True, entry_time, position
    
    def leave(self, car_id):
        """车辆离开停车场"""
        exit_time = datetime.now()
        target = None
        
        # 查找目标车辆并移动后续车辆
        while self.stack:
            car_id_entry = self.stack.pop()
            if car_id_entry[0] == car_id:
                target = {'car_id': car_id_entry[0], 'entry_time': car_id_entry[1]}
                break
            self.temp_stack.append(car_id_entry)
        
        # 未找到车辆
        if not target:
            # 恢复临时栈中的车辆
            while self.temp_stack:
                self.stack.append(self.temp_stack.pop())
            return False, exit_time, "车辆不存在"
        
        # 计算停留时间和费用
        duration = (exit_time - target['entry_time']).total_seconds()
        fee, minutes = calculate_fee(target['entry_time'], exit_time)
        
        # 恢复临时栈中的车辆
        while self.temp_stack:
            self.stack.append(self.temp_stack.pop())
        
        self.notify_observers()
        return True, {
            'car_id': car_id,
            'position': target.get('position', None),
            'entry_time': target['entry_time'],
            'exit_time': exit_time,
            'fee': fee,
            'minutes': minutes
        }
    
    def get_status(self):
        """获取当前停车场状态"""
        return [
            {
                'plate': str(car[0]), 
                'minutes': int((datetime.now() - car[1]).total_seconds() // 60)
            }
            for car in self.stack
        ]