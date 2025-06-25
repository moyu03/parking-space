from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QGroupBox

class SideRoadList(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        self.queue_label = QLabel("便道排队: 0辆车")
        
        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(120)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        
        layout.addWidget(self.queue_label)
        layout.addWidget(self.list_widget)
    
    def update_queue(self, queue_data):
        """更新便道队列显示"""
        self.queue_label.setText(f"便道排队: {len(queue_data)}辆车")
        self.list_widget.clear()
        
        for i, car in enumerate(queue_data):
            self.list_widget.addItem(f"{i+1}. {car['car_id']}")