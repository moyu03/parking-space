from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator

class ControlPanel(QWidget):
    arrive_signal = pyqtSignal(str)
    leave_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # 车牌输入框
        self.input_plate = QLineEdit()
        self.input_plate.setPlaceholderText("请输入车牌号")
        self.input_plate.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9]{3,8}"), self))
        
        # 按钮组
        btn_layout = QHBoxLayout()
        self.btn_arrive = QPushButton("车辆到达")
        self.btn_leave = QPushButton("车辆离开")
        self.btn_refresh = QPushButton("刷新")
        
        # 按钮样式
        self.btn_arrive.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px;")
        self.btn_leave.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        
        # 信息显示
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        
        # 布局
        layout.addWidget(QLabel("车牌操作:"))
        layout.addWidget(self.input_plate)
        btn_layout.addWidget(self.btn_arrive)
        btn_layout.addWidget(self.btn_leave)
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)
        layout.addWidget(self.info_label)
        
        # 连接信号
        self.btn_arrive.clicked.connect(self.handle_arrive)
        self.btn_leave.clicked.connect(self.handle_leave)
        self.btn_refresh.clicked.connect(self.request_refresh)
        
        self.setLayout(layout)
    
    def handle_arrive(self):
        """处理到达按钮点击"""
        plate = self.input_plate.text().strip()
        if plate:
            self.arrive_signal.emit(plate)
            self.input_plate.clear()
    
    def handle_leave(self):
        """处理离开按钮点击"""
        plate = self.input_plate.text().strip()
        if plate:
            self.leave_signal.emit(plate)
            self.input_plate.clear()
    
    def show_message(self, msg):
        """显示操作反馈"""
        self.info_label.setText(msg)
        self.info_label.setStyleSheet("color: green;")
    
    def show_error(self, msg):
        """显示错误信息"""
        self.info_label.setText(f"错误: {msg}")
        self.info_label.setStyleSheet("color: red;")
    
    def request_refresh(self):
        """请求刷新数据"""
        # 发送刷新信号...