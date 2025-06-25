from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from src.ui.status_panel import StatusPanel
from src.ui.control_panel import ControlPanel
from src.ui.fee_display import FeeDisplay
from src.ui.status_panel import StatusPanel

class MainWindow(QMainWindow):
    def __init__(self, parking_service, side_road):
        super().__init__()
        self.parking_service = parking_service
        self.side_road = side_road
        self.setWindowTitle("停车场管理系统")
        
        # 初始化所有组件
        self.status_panel = StatusPanel()
        self.control_panel = ControlPanel()
        self.fee_display = FeeDisplay()
        
        # 设置主布局
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.status_panel)  # 顶部：状态面板
        layout.addWidget(self.fee_display)   # 中部：费用显示
        layout.addWidget(self.control_panel) # 底部：控制面板
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)  # 新增设置中心部件
        
        # 连接信号
        self.control_panel.arrive_signal.connect(self.handle_arrival)
        self.control_panel.leave_signal.connect(self.handle_departure)
        
    def handle_arrival(self, plate):
        success, _, _ = self.parking_service.enter(plate)
        if not success:
            self.show_warning("停车场已满，车辆进入便道等候")
        else:
            self.status_panel.update_status(
                self.parking_service.get_parking_data(),
                self.side_road.get_queue_data()
            )
    
    def handle_departure(self, plate):
        result = self.parking_service.leave(plate)
        if isinstance(result[1], dict):
            success, detail = result
        else:
            success = result[0]
            detail = result[2]
        if success:
            self.fee_display.show_fee(detail['fee'], detail['minutes'])
            self.status_panel.update_status(
                self.parking_service.get_parking_data(),
                self.side_road.get_queue_data()
            )
        else:
            self.show_error("车辆不存在")
    
    def show_error(self, msg):
        QMessageBox.critical(self, '错误', msg)