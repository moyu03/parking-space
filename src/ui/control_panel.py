from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QProgressBar, QHBoxLayout, QGroupBox
)
from PyQt5.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 输入区域
        input_group = QGroupBox("车辆操作")
        input_layout = QVBoxLayout(input_group)
        
        self.input_plate = QLineEdit()
        self.input_plate.setPlaceholderText("请输入车牌号(如:粤A12345)")
        
        btn_layout = QHBoxLayout()
        self.btn_arrive = QPushButton("车辆到达")
        self.btn_leave = QPushButton("车辆离开")
        self.btn_refresh = QPushButton("刷新状态")
        
        btn_layout.addWidget(self.btn_arrive)
        btn_layout.addWidget(self.btn_leave)
        btn_layout.addWidget(self.btn_refresh)
        
        input_layout.addWidget(QLabel("车牌号码:"))
        input_layout.addWidget(self.input_plate)
        input_layout.addLayout(btn_layout)
        
        # 容量指示器
        capacity_group = QGroupBox("停车场状态")
        capacity_layout = QVBoxLayout(capacity_group)
        
        capacity_info = QLabel("当前停车场占用率:")
        self.capacity_bar = QProgressBar()
        self.capacity_bar.setRange(0, 100)
        self.capacity_bar.setTextVisible(True)
        self.capacity_bar.setAlignment(Qt.AlignCenter)
        
        capacity_layout.addWidget(capacity_info)
        capacity_layout.addWidget(self.capacity_bar)
        
        # 添加到主布局
        main_layout.addWidget(input_group)
        main_layout.addWidget(capacity_group)
        main_layout.addStretch()
        
        # 设置样式
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #95a5a6;
                border-radius: 6px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)