# core/parking.py

import time
from collections import deque

class Car:
    def __init__(self, car_id):
        self.car_id = car_id
        self.enter_time = time.time()

    def get_duration(self):
        return time.time() - self.enter_time

class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.stack = []  # 停车场是栈
        self.temp_stack = []  # 临时出场

    def is_full(self):
        return len(self.stack) >= self.capacity

    def arrive(self, car: Car):
        if self.is_full():
            return False
        self.stack.append(car)
        return True

    def depart(self, car_id):
        found = False
        while self.stack:
            top = self.stack[-1]
            if top.car_id == car_id:
                found = True
                target = self.stack.pop()
                break
            else:
                self.temp_stack.append(self.stack.pop())

        if not found:
            while self.temp_stack:
                self.stack.append(self.temp_stack.pop())
            return None

        while self.temp_stack:
            self.stack.append(self.temp_stack.pop())

        return target

    def current_state(self):
        return [(car.car_id, car.enter_time) for car in self.stack]

class WaitingLane:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = deque()

    def is_full(self):
        return len(self.queue) >= self.capacity

    def enqueue(self, car: Car):
        if self.is_full():
            return False
        self.queue.append(car)
        return True

    def dequeue(self):
        if not self.queue:
            return None
        return self.queue.popleft()

    def current_state(self):
        return [(car.car_id, car.enter_time) for car in self.queue]
