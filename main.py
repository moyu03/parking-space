import sys
import time
from PyQt5.QtWidgets import QApplication
 #from core.parking_lot import ParkingSystem
from ui.main_window import MainWindow

def main():
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 初始化核心系统
    #parking_system = ParkingSystem(capacity=10)
    
    # 创建主窗口
    window = MainWindow(parking_system)
    window.show()
    
    # 执行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()