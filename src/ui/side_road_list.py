from PyQt5.QtWidgets import QListWidget
import time

class SideRoadList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
        """)
    
    def update_queue(self, side_road_data):
        """更新便道队列显示"""
        self.clear()
        
        if not side_road_data:
            self.addItem("便道空闲")
            return
        
        for i, car in enumerate(side_road_data):
            # 显示：1. 京A12345 (等待10分钟)
            # arrival_time = time.strftime("%H:%M", car['arrival_time'])
            try:
                self.addItem(f"{i+1}. {car['car_id']} (等待中)")
            except TypeError:
                self.addItem(f"{i+1}. {car} (等待中)")
