from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel

class FeeDisplay(QGroupBox):
    def __init__(self):
        super().__init__("费用信息")
        self.setFixedHeight(120)
        
        layout = QGridLayout(self)
        
        # 创建显示标签
        fee_title = QLabel("本次费用:")
        time_title = QLabel("停留时间:")
        
        self.fee_value = QLabel("0.0元")
        self.time_value = QLabel("0.0分钟")
        
        # 设置样式
        for label in [self.fee_value, self.time_value]:
            label.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    color: #e74c3c;
                    font-weight: bold;
                }
            """)
        
        # 布局
        layout.addWidget(fee_title, 0, 0)
        layout.addWidget(self.fee_value, 0, 1)
        layout.addWidget(time_title, 1, 0)
        layout.addWidget(self.time_value, 1, 1)
    
    def display_fee(self, fee, duration):
        """显示费用信息"""
        self.fee_value.setText(f"{fee:.2f}元")
        self.time_value.setText(f"{duration:.1f}分钟")