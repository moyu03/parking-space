# main.py
import sys
from PyQt5.QtWidgets import QApplication
from src.core.parking_lot import ParkingLot
from src.core.side_road import SideRoad
from src.ui.main_window import MainWindow

def main():
    # 初始化核心系统
    parking_system = ParkingLot()
    side_road = SideRoad()
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow(parking_system, side_road)
    window.show()
    
    # 启动应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()