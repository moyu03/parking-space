from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class FeeDisplay(QGroupBox):
    def __init__(self):
        super().__init__("费用信息")
        layout = QVBoxLayout()
        self.fee_label = QLabel("当前费用：0元")
        self.duration_label = QLabel("停车时长：0分钟")
        layout.addWidget(self.fee_label)
        layout.addWidget(self.duration_label)
        self.setLayout(layout)

    def show_fee(self, fee, minutes):
        self.fee_label.setText(f"当前费用：{fee}元")
        self.duration_label.setText(f"停车时长：{minutes}分钟")