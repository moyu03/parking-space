from datetime import datetime

class SideRoad:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, car_id):
        """车辆进入便道"""
        if len(self.queue) >= SIDE_ROAD_LIMIT:
            return False, datetime.now(), "便道已满"
        
        position = len(self.queue) + 1
        arrival_time = datetime.now()
        self.queue.append({
            'car_id': car_id,
            'arrival_time': arrival_time,
            'position': position
        })
        return True, arrival_time, position
    
    def dequeue(self):
        """车辆离开便道"""
        if not self.queue:
            return None
        return self.queue.pop(0)
    
    def get_queue_data(self):
        """获取便道队列数据"""
        return {
            'current': len(self.queue),
            'vehicles': [car['car_id'] for car in self.queue]
        }

    def get_status(self):
        """获取当前便道状态"""
        return [dict(v) for v in self.queue]