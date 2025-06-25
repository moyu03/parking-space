from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from src.core.calculator import format_duration

class ParkingTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["车牌号", "位置", "停留时间"])
        
    def update_data(self, parking_data):
        """更新表格数据"""
        self.setRowCount(len(parking_data))
        
        for row, car in enumerate(parking_data):
            # 停留时间格式化：1小时15分
            duration = format_duration(car['minutes'])
            
            self.setItem(row, 0, QTableWidgetItem(car['plate']))
            self.setItem(row, 1, QTableWidgetItem(str(car['minutes'])))
            self.setItem(row, 2, QTableWidgetItem(duration))
    
    def highlight_car(self, car_id):
        """高亮显示指定车辆"""
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == car_id:
                for col in range(self.columnCount()):
                    self.item(row, col).setBackground(Qt.yellow)
                break