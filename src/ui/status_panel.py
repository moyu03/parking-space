from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from src.ui.parking_table import ParkingTable
from src.ui.side_road_list import SideRoadList

class StatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # 停车表格
        self.parking_table = ParkingTable()
        layout.addWidget(QLabel("停车场状态"))
        layout.addWidget(self.parking_table)
        
        # 便道列表
        self.side_road_list = SideRoadList()
        layout.addWidget(QLabel("便道等待车辆"))
        layout.addWidget(self.side_road_list)
        
        self.setLayout(layout)
    
    def update_status(self, parking_data, side_road_data):
        """更新界面状态"""
        self.parking_table.update_data(parking_data['vehicles'])
        self.side_road_list.update_queue(side_road_data)