import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QStackedLayout, QWidget, 
    QHBoxLayout, QVBoxLayout, QMenuBar, QStatusBar
)
from .parking_table import ParkingTable
from .control_panel import ControlPanel
from .side_road_list import SideRoadList
from .fee_display import FeeDisplay

class MainWindow(QMainWindow):
    def __init__(self, parking_system):
        super().__init__()
        self.parking_system = parking_system
        self.setWindowTitle("停车场管理系统")
        self.setGeometry(100, 100, 1200, 700)
        
        # 初始化UI组件
        self.init_ui()
        
        # 初始加载数据
        self.update_display()
        
        # 连接信号槽
        self.connect_signals()
    
    def init_ui(self):
        """初始化主界面布局"""
        # 创建中央容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧状态面板
        status_panel = QWidget()
        status_layout = QVBoxLayout(status_panel)
        
        self.parking_table = ParkingTable()
        self.side_road_list = SideRoadList()
        
        status_layout.addWidget(self.parking_table)
        status_layout.addWidget(self.side_road_list)
        
        # 右侧控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        self.control_panel = ControlPanel()
        self.fee_display = FeeDisplay()
        
        control_layout.addWidget(self.control_panel)
        control_layout.addWidget(self.fee_display)
        control_layout.addStretch()
        
        # 添加到主布局
        main_layout.addWidget(status_panel, 70)  # 70%宽度
        main_layout.addWidget(control_panel, 30)  # 30%宽度
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("系统就绪")
        
        # 菜单栏
        self.menu_bar = self.menuBar()
        self.init_menus()
    
    def init_menus(self):
        """初始化菜单系统"""
        # 文件菜单
        file_menu = self.menu_bar.addMenu("文件")
        file_menu.addAction("保存状态", self.save_state)
        file_menu.addAction("加载状态", self.load_state)
        file_menu.addSeparator()
        file_menu.addAction("退出", self.close)
        
        # 操作菜单
        action_menu = self.menu_bar.addMenu("操作")
        action_menu.addAction("手动刷新", self.update_display)
    
    def connect_signals(self):
        """连接信号槽"""
        # 连接按钮事件
        self.control_panel.btn_arrive.clicked.connect(self.on_vehicle_arrive)
        self.control_panel.btn_leave.clicked.connect(self.on_vehicle_leave)
        self.control_panel.btn_refresh.clicked.connect(self.update_display)
    
    def on_vehicle_arrive(self):
        """处理车辆到达事件"""
        plate = self.control_panel.input_plate.text().strip()
        
        if not plate:
            self.show_warning("请输入车牌号")
            return
        
        result = self.parking_system.enter(plate)
        
        if result["status"] == "PARKED":
            self.show_info(f"车辆 {plate} 已停入 #{result['position']} 车位")
        elif result["status"] == "IN_SIDE_ROAD":
            self.show_info(f"车辆 {plate} 进入便道排队 #{result['position']}")
        else:
            self.show_error(f"车辆进入失败: {result.get('message', '未知错误')}")
        
        self.update_display()
    
    def on_vehicle_leave(self):
        """处理车辆离开事件"""
        plate = self.control_panel.input_plate.text().strip()
        
        if not plate:
            self.show_warning("请输入车牌号")
            return
        
        result = self.parking_system.leave(plate)
        
        if result["status"] == "SUCCESS":
            self.show_info(f"车辆 {plate} 已离场")
            self.fee_display.display_fee(result["fee"], result["duration"])
        else:
            self.show_error(f"车辆离场失败: {result.get('message', '未找到车辆')}")
        
        self.update_display()
    
    def update_display(self):
        """更新所有显示组件"""
        status = self.parking_system.get_status()
        
        # 更新停车场表格
        self.parking_table.update_data(status["parking_spots"])
        
        # 更新便道列表
        self.side_road_list.update_queue(status["side_road"])
        
        # 更新容量进度条
        occupancy = status["occupied_count"] / status["parking_capacity"] * 100
        self.control_panel.capacity_bar.setValue(int(occupancy))
        
        # 更新状态栏信息
        self.status_bar.showMessage(
            f"总车位: {status['parking_capacity']} | "
            f"已用: {status['occupied_count']} | "
            f"便道等待: {status['side_road_count']} | "
            f"更新时间: {time.strftime('%H:%M:%S', time.localtime(status['timestamp']))}"
        )
    
    def show_info(self, message):
        """显示信息提示"""
        self.status_bar.showMessage(message)
        # 或者使用消息框: QMessageBox.information(self, "提示", message)
    
    def show_warning(self, message):
        """显示警告信息"""
        self.status_bar.showMessage("警告: " + message, 5000)
    
    def show_error(self, message):
        """显示错误信息"""
        self.status_bar.showMessage("错误: " + message, 5000)
    
    def save_state(self):
        """保存系统状态（通过文件菜单调用）"""
        # 实际调用核心模块的保存功能
    
    def load_state(self):
        """加载系统状态（通过文件菜单调用）"""
        # 实际调用核心模块的加载功能