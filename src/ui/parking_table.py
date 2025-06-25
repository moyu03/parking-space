from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class ParkingTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["车牌号", "车位", "进入时间", "停留时间"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setMinimumHeight(400)
        
        # 设置表格样式
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 4px;
            }
        """)
    
    def update_data(self, parking_data):
        """更新表格数据"""
        self.setRowCount(len(parking_data))
        
        for row, car in enumerate(parking_data):
            # 时间格式转换
            entry_time = time.strftime("%H:%M:%S", time.localtime(car["entry_time"]))
            duration = f"{car['duration']:.1f}分" if car.get('duration') else "-"
            
            # 填充表格项
            self.setItem(row, 0, QTableWidgetItem(car["car_id"]))
            self.setItem(row, 1, QTableWidgetItem(f"#{car['position']}"))
            self.setItem(row, 2, QTableWidgetItem(entry_time))
            self.setItem(row, 3, QTableWidgetItem(duration))
    
    def highlight_row(self, car_id):
        """高亮显示指定车辆"""
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == car_id:
                for col in range(self.columnCount()):
                    self.item(row, col).setBackground(Qt.yellow)
                break